"""Главное окно приложения."""

import logging
import sys
from ..database.models import DictionaryDB
from ..processors.synthesizer import MorphoDictionary
from ..processors.text_processor import TextProcessor
from ..benchmark import PerformanceTester
from .mixins import (
    FileTabMixin,
    DictionaryTabMixin,
    SynthesizerTabMixin,
    StorageMixin,
)
from .ui_controller import UIController

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

logger = logging.getLogger(__name__)

class ProcessingThread(QThread):
    """Поток для обработки текста в фоновом режиме."""

    progress = pyqtSignal(int)
    finished = pyqtSignal(list, list)
    error = pyqtSignal(str)

    def __init__(self, text: str, processor: TextProcessor):
        super().__init__()
        self.text = text
        self.processor = processor

    def run(self):
        try:
            logger.debug("Поток обработки: извлечение слов")
            self.progress.emit(10)
            words = self.processor.extract_words(self.text)
            logger.debug(
                "Поток обработки: извлечено слов %d, извлечение словосочетаний",
                len(words),
            )
            self.progress.emit(50)
            collocations = self.processor.extract_collocations(self.text)
            self.progress.emit(100)
            logger.debug(
                "Поток обработки: извлечено словосочетаний %d", len(collocations)
            )
            self.finished.emit(words, collocations)
        except Exception as e:
            logger.exception("Ошибка при обработке текста в потоке: %s", e)
            self.error.emit(str(e))


class MainWindow(
    QMainWindow,
    FileTabMixin,
    DictionaryTabMixin,
    SynthesizerTabMixin,
    StorageMixin,
):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()
        logger.debug("Инициализация MainWindow: подключение к БД")
        self.db = DictionaryDB()
        try:
            self.processor = TextProcessor()
        except RuntimeError as e:
            logger.exception(
                "Ошибка инициализации: не удалось загрузить модель spaCy: %s", e
            )
            QMessageBox.critical(
                None,
                "Ошибка инициализации",
                f"Не удалось загрузить модель spaCy:\n{str(e)}\n\n"
                "Пожалуйста, установите модель командой:\n"
                "python -m spacy download en_core_web_sm",
            )
            sys.exit(1)
        self.current_text = ""
        self.morpho_dictionary = MorphoDictionary()
        self.synthesizer = None
        self.performance_tester = PerformanceTester()

        try:
            self.db.clear_all_dictionary()
            logger.debug("База данных очищена при запуске")
        except Exception as e:
            logger.warning("Очистка БД при запуске: %s", e)

        logger.debug("Инициализация UI")
        self._ui = UIController(self)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle("Словарь словосочетаний - Задание 3")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.addWidget(self._ui.create_toolbar())

        tabs = QTabWidget()
        tabs.addTab(self.create_file_tab(), "Загрузка файла")
        tabs.addTab(self.create_dictionary_tab(), "Словарь")
        tabs.addTab(self.create_synthesizer_tab(), "Синтез")
        tabs.addTab(self.create_benchmark_tab(), "Тестирование")
        tabs.addTab(self._ui.create_terminology_tab(), "Терминология")
        tabs.addTab(self._ui.create_help_tab(), "Помощь")
        main_layout.addWidget(tabs)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage(
            "Готово. БД очищена при запуске; для сохранения используйте «Экспорт словаря»."
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.statusbar.addPermanentWidget(self.progress_bar)

    def process_text(self):
        """Обрабатывает текст и извлекает словосочетания."""
        text = self.text_edit.toPlainText()
        logger.debug("Запуск обработки текста, длина: %d символов", len(text))
        if not text.strip():
            logger.warning("Попытка обработки пустого текста")
            QMessageBox.warning(self, "Ошибка", "Текст для обработки пуст")
            return

        self.current_text = text
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusbar.showMessage("Обработка текста...")

        # Запуск обработки в отдельном потоке
        self.processing_thread = ProcessingThread(text, self.processor)
        self.processing_thread.progress.connect(self.progress_bar.setValue)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.start()

    def on_processing_finished(self, words: list, collocations: list):
        """Обработчик завершения обработки текста."""
        self.progress_bar.setVisible(False)
        logger.debug(
            "Обработка текста завершена: слов=%d, словосочетаний=%d",
            len(words),
            len(collocations),
        )
        try:
            for lemma, pos in words:
                self.db.add_word(lemma, pos)

            collocation_dict = {}
            for phrase, frequency in collocations:
                if phrase in collocation_dict:
                    collocation_dict[phrase] += frequency
                else:
                    collocation_dict[phrase] = frequency

            logger.debug(
                "Обработка %d уникальных словосочетаний", len(collocation_dict)
            )
            for phrase, total_frequency in collocation_dict.items():
                word_lemmas = phrase.split()

                if word_lemmas:
                    try:
                        self.db.add_collocation(
                            phrase,
                            word_lemmas,
                            total_frequency,
                            self.current_text[:100],
                        )
                    except Exception as e:
                        logger.warning(
                            "Ошибка при добавлении словосочетания '%s': %s", phrase, e
                        )

            self.statusbar.showMessage(
                f"Обработано: {len(words)} слов, {len(collocations)} словосочетаний"
            )
            QMessageBox.information(
                self,
                "Успех",
                f"Текст обработан успешно!\n"
                f"Найдено слов: {len(words)}\n"
                f"Найдено словосочетаний: {len(collocations)}",
            )

            logger.debug("Данные сохранены в БД, обновление таблицы словаря")
            self.refresh_dictionary_table()
        except Exception as e:
            logger.exception("Ошибка при сохранении в базу данных: %s", e)
            QMessageBox.critical(
                self, "Ошибка", f"Ошибка при сохранении в базу данных:\n{str(e)}"
            )

    def on_processing_error(self, error_msg: str):
        """Обработчик ошибки обработки."""
        logger.error("Ошибка обработки текста: %s", error_msg)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(
            self, "Ошибка обработки", f"Произошла ошибка:\n{error_msg}"
        )
        self.statusbar.showMessage("Ошибка обработки")

    def create_benchmark_tab(self):
        """Создает вкладку для тестирования производительности."""
        from PyQt6.QtWidgets import (
            QGroupBox,
            QTextEdit,
            QLabel,
        )

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Группа тестов
        test_group = QGroupBox("Тестирование производительности")
        test_layout = QVBoxLayout(test_group)

        # Описание
        desc_label = QLabel(
            "Запустите тесты для измерения времени выполнения основных операций. "
            "Результаты покажут скорость обработки текста, поиска и других операций."
        )
        desc_label.setWordWrap(True)
        test_layout.addWidget(desc_label)

        # Кнопки тестов
        buttons_layout = QHBoxLayout()

        btn_test_text = QPushButton("Тест обработки текста")
        btn_test_text.clicked.connect(self.run_text_processing_benchmark)
        buttons_layout.addWidget(btn_test_text)

        btn_test_search = QPushButton("Тест поиска")
        btn_test_search.clicked.connect(self.run_search_benchmark)
        buttons_layout.addWidget(btn_test_search)

        btn_test_filter = QPushButton("Тест фильтрации")
        btn_test_filter.clicked.connect(self.run_filter_benchmark)
        buttons_layout.addWidget(btn_test_filter)

        buttons_layout.addStretch()
        test_layout.addLayout(buttons_layout)

        # Результаты
        results_group = QGroupBox("Результаты тестирования")
        results_layout = QVBoxLayout(results_group)
        self.benchmark_results = QTextEdit()
        self.benchmark_results.setReadOnly(True)
        self.benchmark_results.setPlaceholderText("Результаты тестов появятся здесь...")
        results_layout.addWidget(self.benchmark_results)
        test_layout.addWidget(results_group)

        layout.addWidget(test_group)
        layout.addStretch()
        return widget

    def run_text_processing_benchmark(self):
        """Тест производительности обработки текста."""
        test_texts = {
            "Короткий (100 слов)": "The quick brown fox jumps over the lazy dog. " * 10,
            "Средний (1000 слов)": "The quick brown fox jumps over the lazy dog. "
            * 100,
            "Длинный (5000 слов)": "The quick brown fox jumps over the lazy dog. "
            * 500,
        }
        result = self.performance_tester.test_text_processing(
            self.processor, test_texts
        )
        self.benchmark_results.setText(result)

    def run_search_benchmark(self):
        """Тест производительности поиска."""
        words = self.db.get_all_words()
        queries = ["a", "ab", "abc", "test", "nonexistent"]
        result = self.performance_tester.test_search_performance(
            self.db, words, queries
        )
        self.benchmark_results.setText(result)

    def run_filter_benchmark(self):
        """Тест производительности фильтрации."""
        words = self.db.get_all_words()
        pos_list = ["NOUN", "VERB", "ADJ", "ADV", "PROPN"]
        text_prefixes = ["a", "ab", "abc", "b", "c", "th", "the"]
        result = self.performance_tester.test_filter_performance(
            words, pos_list, text_prefixes
        )
        self.benchmark_results.setText(result)

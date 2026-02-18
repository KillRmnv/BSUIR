"""Миксин для вкладки 'Синтез'."""

import logging

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QGroupBox,
    QMessageBox,
    QWidget,
)

from ...processors.synthesizer import MorphoDictionary, RandomSynthesizer

logger = logging.getLogger(__name__)


class SynthesizerTabMixin:
    """Миксин для работы с вкладкой синтеза."""

    def create_synthesizer_tab(self) -> QWidget:
        """Создает вкладку 'Синтез': загрузка морфо-словаря и генерация словосочетаний."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        source_group = QGroupBox("Источник слов для синтеза")
        source_layout = QVBoxLayout(source_group)
        source_btn_layout = QHBoxLayout()
        btn_load_from_text = QPushButton("Загрузить из текущего текста")
        btn_load_from_text.clicked.connect(self.load_morpho_from_text)
        source_btn_layout.addWidget(btn_load_from_text)
        btn_load_from_db = QPushButton("Загрузить из словаря")
        btn_load_from_db.clicked.connect(self.load_morpho_from_db)
        source_btn_layout.addWidget(btn_load_from_db)
        source_btn_layout.addStretch()
        source_layout.addLayout(source_btn_layout)
        self.morpho_status_label = QLabel("Слов в морфо-словаре: 0")
        source_layout.addWidget(self.morpho_status_label)
        layout.addWidget(source_group)

        synth_group = QGroupBox("Синтез словосочетания")
        synth_layout = QVBoxLayout(synth_group)
        btn_synthesize = QPushButton("Синтезировать словосочетание")
        btn_synthesize.clicked.connect(self.run_synthesize)
        synth_layout.addWidget(btn_synthesize)
        self.synthesizer_result_edit = QLineEdit()
        self.synthesizer_result_edit.setReadOnly(True)
        self.synthesizer_result_edit.setPlaceholderText(
            "Результат синтеза появится здесь..."
        )
        synth_layout.addWidget(self.synthesizer_result_edit)
        layout.addWidget(synth_group)
        layout.addStretch()
        return widget

    def load_morpho_from_text(self):
        """Загружает морфо-словарь из текста на вкладке 'Загрузка файла'."""
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Текст для загрузки пуст. Введите или загрузите текст на вкладке 'Загрузка файла'.",
            )
            return
        try:
            words = self.processor.extract_words(text)
            self.morpho_dictionary = MorphoDictionary()
            self.morpho_dictionary.load_words(words)
            self.synthesizer = RandomSynthesizer(self.morpho_dictionary)
            n = len(self.morpho_dictionary.entries)
            self.morpho_status_label.setText(f"Слов в морфо-словаре: {n}")
            self.statusbar.showMessage(f"Морфо-словарь загружен из текста: {n} слов")
            logger.debug("Морфо-словарь загружен из текста: %d слов", n)
        except Exception as e:
            logger.exception("Ошибка загрузки морфо-словаря из текста: %s", e)
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить слова из текста:\n{str(e)}"
            )

    def load_morpho_from_db(self):
        """Загружает морфо-словарь из слов, сохранённых в словаре (БД)."""
        try:
            words = self.db.get_all_words()
            word_list = [
                (w.lemma, w.pos or "")
                for w in words
                if w.pos in ("NOUN", "VERB", "ADJ", "ADV")
            ]
            self.morpho_dictionary = MorphoDictionary()
            self.morpho_dictionary.load_words(word_list)
            self.synthesizer = RandomSynthesizer(self.morpho_dictionary)
            n = len(self.morpho_dictionary.entries)
            self.morpho_status_label.setText(f"Слов в морфо-словаре: {n}")
            self.statusbar.showMessage(f"Морфо-словарь загружен из словаря: {n} слов")
            logger.debug("Морфо-словарь загружен из БД: %d слов", n)
        except Exception as e:
            logger.exception("Ошибка загрузки морфо-словаря из БД: %s", e)
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить слова из словаря:\n{str(e)}"
            )

    def run_synthesize(self):
        """Запускает синтез словосочетания и выводит результат."""
        if not self.morpho_dictionary.entries:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Морфо-словарь пуст. Загрузите слова из текста или из словаря (кнопки выше).",
            )
            return
        try:
            result = self.synthesizer.synthesize()
            self.synthesizer_result_edit.setText(result)
            self.statusbar.showMessage("Синтез выполнен")
            logger.debug("Синтез словосочетания: %s", result)
        except Exception as e:
            logger.exception("Ошибка синтеза: %s", e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при синтезе:\n{str(e)}")

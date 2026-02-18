"""Миксин для вкладки 'Загрузка файла'."""

import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QLabel,
    QGroupBox,
)

from ...readers.reader_factory import ReaderFactory

logger = logging.getLogger(__name__)


class FileTabMixin:
    """Миксин для работы с вкладкой загрузки файла."""

    def create_file_tab(self) -> "QWidget":
        """Создает вкладку для загрузки и обработки файлов."""
        from PyQt6.QtWidgets import QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        file_group = QGroupBox("Загрузка файла")
        file_layout = QVBoxLayout(file_group)

        file_btn_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Выберите файл для обработки...")
        file_btn_layout.addWidget(self.file_path_edit)

        btn_browse = QPushButton("Обзор...")
        btn_browse.clicked.connect(self.browse_file)
        file_btn_layout.addWidget(btn_browse)
        file_layout.addLayout(file_btn_layout)

        btn_load = QPushButton("Загрузить файл")
        btn_load.clicked.connect(self.load_file)
        file_layout.addWidget(btn_load)
        layout.addWidget(file_group)

        text_group = QGroupBox("Текст для обработки")
        text_layout = QVBoxLayout(text_group)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введите текст или загрузите файл...")
        text_layout.addWidget(self.text_edit)
        layout.addWidget(text_group)

        self.text_info_label = QLabel("Статистика: 0 слов")
        layout.addWidget(self.text_info_label)

        # Кнопка обработки текста внизу вкладки
        btn_process = QPushButton("Обработать текст")
        btn_process.setStyleSheet(
            "QPushButton { font-weight: bold; padding: 10px; font-size: 12px; }"
        )
        btn_process.clicked.connect(self.process_text)
        layout.addWidget(btn_process)

        return widget

    def browse_file(self):
        """Открывает диалог выбора файла."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все поддерживаемые (*.txt *.rtf *.pdf *.doc *.docx);;"
            "Текстовые файлы (*.txt);;"
            "RTF файлы (*.rtf);;"
            "PDF файлы (*.pdf);;"
            "Word документы (*.doc *.docx)",
        )
        if file_path:
            self.file_path_edit.setText(file_path)

    def load_file(self):
        """Загружает файл и отображает его содержимое."""
        file_path = self.file_path_edit.text()
        logger.debug("Загрузка файла: %s", file_path or "(не указан)")
        if not file_path:
            logger.warning("Попытка загрузки без выбранного файла")
            QMessageBox.warning(self, "Ошибка", "Выберите файл для загрузки")
            return

        try:
            reader = ReaderFactory.create_reader(Path(file_path))
            text = reader.read()
            self.text_edit.setPlainText(text)
            self.current_text = text

            word_count = len(text.split())
            self.text_info_label.setText(
                f"Статистика: {word_count} слов, {len(text)} символов"
            )
            self.statusbar.showMessage(f"Файл загружен: {Path(file_path).name}")
            logger.debug(
                "Файл загружен успешно: %d слов, %d символов", word_count, len(text)
            )
        except Exception as e:
            logger.exception("Не удалось загрузить файл %s: %s", file_path, e)
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}"
            )

    def open_and_load_file(self):
        """Открывает диалог выбора файла и сразу загружает его."""
        logger.debug("Открытие диалога выбора файла")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все поддерживаемые (*.txt *.rtf *.pdf *.doc *.docx);;"
            "Текстовые файлы (*.txt);;"
            "RTF файлы (*.rtf);;"
            "PDF файлы (*.pdf);;"
            "Word документы (*.doc *.docx)",
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.load_file()

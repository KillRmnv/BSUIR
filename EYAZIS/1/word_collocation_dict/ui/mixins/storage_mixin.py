"""Миксин для операций с хранилищем (импорт, экспорт, очистка)."""

import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from ...storage.factory import StorageFactory

logger = logging.getLogger(__name__)


class StorageMixin:
    """Миксин для работы с импортом/экспортом/очисткой словаря."""

    def export_dictionary(self):
        """Экспортирует словарь в файл."""
        exts = StorageFactory.get_supported_export_extensions()
        filter_str = ";;".join(f"Файлы (*{e})" for e in exts)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт словаря", "", filter_str
        )
        if not file_path:
            return
        logger.debug("Экспорт словаря в файл: %s", file_path)
        exporter = StorageFactory.get_exporter(Path(file_path))
        if not exporter:
            QMessageBox.critical(self, "Ошибка", "Неподдерживаемый формат файла.")
            return
        try:
            words = self.db.get_all_words()
            exporter.export(Path(file_path), words)
            full_path = Path(file_path).absolute()
            file_size = full_path.stat().st_size
            QMessageBox.information(
                self,
                "Успех",
                f"Словарь экспортирован успешно!\n\n"
                f"Файл: {full_path}\n"
                f"Слов: {len(words)}\n"
                f"Размер: {file_size} байт",
            )
        except Exception as e:
            logger.exception("Ошибка при экспорте словаря: %s", e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте:\n{str(e)}")

    def _load_dictionary_from_file(self, merge: bool) -> None:
        """Загружает словарь из файла. merge=True — добавить к текущему."""
        exts = StorageFactory.get_supported_import_extensions()
        filter_str = ";;".join(f"Файлы (*{e})" for e in exts)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл словаря", "", filter_str
        )
        if not file_path:
            return
        importer = StorageFactory.get_importer(Path(file_path))
        if not importer:
            QMessageBox.critical(self, "Ошибка", "Неподдерживаемый формат файла.")
            return
        try:
            data = importer.load(Path(file_path))
            if not merge:
                self.db.clear_all_dictionary()
            for lemma, pos, collocations in data:
                self.db.add_word(lemma, pos or None)
                for phrase, freq in collocations:
                    word_lemmas = phrase.split()
                    if word_lemmas:
                        try:
                            self.db.add_collocation(phrase, word_lemmas, freq, None)
                        except Exception as e:
                            logger.warning(
                                "Ошибка при добавлении словосочетания '%s': %s",
                                phrase,
                                e,
                            )
            self.refresh_dictionary_table()
            self.collocation_table.setRowCount(0)
            mode = "добавлен к текущему" if merge else "загружен (текущий заменён)"
            QMessageBox.information(
                self, "Успех", f"Словарь {mode}.\nЗагружено записей: {len(data)}"
            )
        except Exception as e:
            logger.exception("Ошибка при импорте словаря: %s", e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при импорте:\n{str(e)}")

    def import_dictionary(self):
        """Импорт словаря из файла (заменяет текущий)."""
        self._load_dictionary_from_file(merge=False)

    def stack_dictionary(self):
        """Добавить словарь из файла к текущему."""
        self._load_dictionary_from_file(merge=True)

    def clear_dictionary(self):
        """Очищает весь словарь."""
        words = self.db.get_all_words()
        word_count = len(words)
        total_collocations = sum(len(w.collocations) for w in words)

        if word_count == 0:
            QMessageBox.information(self, "Информация", "Словарь уже пуст.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите полностью очистить словарь?\n\n"
            f"Будет удалено:\n"
            f"  • Слов: {word_count}\n"
            f"  • Словосочетаний: {total_collocations}\n\n"
            f"Это действие нельзя отменить!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            logger.debug("Очистка словаря: удаление всех записей")
            try:
                deleted_words, deleted_collocations = self.db.clear_all_dictionary()
                logger.debug(
                    "Словарь очищен: удалено слов=%d, словосочетаний=%d",
                    deleted_words,
                    deleted_collocations,
                )

                self.refresh_dictionary_table()
                self.collocation_table.setRowCount(0)

                self.statusbar.showMessage(
                    f"Словарь очищен: удалено {deleted_words} слов и {deleted_collocations} словосочетаний"
                )
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Словарь успешно очищен!\n\n"
                    f"Удалено:\n"
                    f"  • Слов: {deleted_words}\n"
                    f"  • Словосочетаний: {deleted_collocations}",
                )
            except Exception as e:
                logger.exception("Ошибка при очистке словаря: %s", e)
                QMessageBox.critical(
                    self, "Ошибка", f"Ошибка при очистке словаря:\n{str(e)}"
                )

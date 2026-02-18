"""Миксин для редактирования словаря (добавление/удаление)."""

import logging

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QLabel,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDialog,
    QFormLayout,
)

from ...database.models import Word, Collocation

logger = logging.getLogger(__name__)


class DictionaryEditMixin:
    """Миксин для добавления и удаления слов/словосочетаний."""

    def add_word_dialog(self):
        """Открывает диалог для добавления нового слова (леммы)."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить слово")
        dialog.setMinimumWidth(300)

        layout = QFormLayout(dialog)

        # Поле для леммы
        lemma_input = QLineEdit()
        lemma_input.setPlaceholderText("Введите слово (лемму)...")
        layout.addRow("Лемма:", lemma_input)

        # Выпадающий список для части речи (non-editable)
        pos_input = QComboBox()
        pos_input.addItems(["NOUN", "VERB", "ADJ", "ADV", "PROPN"])
        pos_input.setEditable(False)
        layout.addRow("Часть речи:", pos_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("Добавить")
        btn_cancel = QPushButton("Отмена")
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        layout.addRow(buttons_layout)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            lemma = lemma_input.text().strip().lower()
            pos = pos_input.currentText().strip()

            if not lemma:
                QMessageBox.warning(self, "Ошибка", "Введите лемму слова")
                return

            # Валидация части речи
            valid_pos = ["NOUN", "VERB", "ADJ", "ADV", "PROPN"]
            if pos not in valid_pos:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Неверная часть речи '{pos}'.\n\n"
                    f"Допустимые значения: {', '.join(valid_pos)}",
                )
                return

            # Проверка на дубликаты
            existing = self.db.get_session().query(Word).filter_by(lemma=lemma).first()
            if existing:
                QMessageBox.warning(
                    self, "Ошибка", f"Слово '{lemma}' уже существует в словаре"
                )
                return

            try:
                self.db.add_word(lemma, pos)
                self.refresh_dictionary_table()
                self.statusbar.showMessage(f"Слово '{lemma}' добавлено")
                logger.debug("Добавлено слово: %s (%s)", lemma, pos)
            except Exception as e:
                logger.exception("Ошибка при добавлении слова '%s': %s", lemma, e)
                QMessageBox.critical(
                    self, "Ошибка", f"Ошибка при добавлении слова:\n{str(e)}"
                )

    def delete_selected_word(self):
        """Удаляет выбранное слово из словаря."""
        current_row = self.dict_table.currentRow()
        if current_row < 0:
            logger.warning("Попытка удаления слова без выбора")
            QMessageBox.warning(self, "Ошибка", "Выберите слово для удаления")
            return

        lemma = self.dict_table.item(current_row, 0).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить слово '{lemma}' и все его словосочетания?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            logger.debug("Удаление слова из словаря: %s", lemma)
            try:
                if self.db.delete_word(lemma):
                    logger.debug("Слово удалено: %s", lemma)
                    self.refresh_dictionary_table()
                    self.statusbar.showMessage(f"Слово '{lemma}' удалено")
                else:
                    logger.warning("Слово для удаления не найдено: %s", lemma)
                    QMessageBox.warning(self, "Ошибка", f"Слово '{lemma}' не найдено")
            except Exception as e:
                logger.exception("Ошибка при удалении слова '%s': %s", lemma, e)
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении:\n{str(e)}")

    def delete_selected_collocation(self):
        """Удаляет выбранное словосочетание."""
        current_row = self.collocation_table.currentRow()
        if current_row < 0:
            logger.warning("Попытка удаления словосочетания без выбора")
            QMessageBox.warning(self, "Ошибка", "Выберите словосочетание для удаления")
            return

        phrase = self.collocation_table.item(current_row, 0).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить словосочетание '{phrase}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            logger.debug("Удаление словосочетания: %s", phrase)
            try:
                if self.db.delete_collocation(phrase):
                    logger.debug("Словосочетание удалено: %s", phrase)
                    selected_row = self.dict_table.currentRow()
                    if selected_row >= 0:
                        lemma = self.dict_table.item(selected_row, 0).text()
                        self.show_word_collocations_for_lemma(lemma)
                    self.refresh_dictionary_table()
                    self.statusbar.showMessage(f"Словосочетание '{phrase}' удалено")
                else:
                    logger.warning("Словосочетание для удаления не найдено: %s", phrase)
                    QMessageBox.warning(
                        self, "Ошибка", f"Словосочетание '{phrase}' не найдено"
                    )
            except Exception as e:
                logger.exception(
                    "Ошибка при удалении словосочетания '%s': %s", phrase, e
                )
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении:\n{str(e)}")

    def _get_default_phrase(self) -> str:
        """Возвращает начальное значение для поля словосочетания."""
        current_row = self.dict_table.currentRow()
        if current_row >= 0:
            lemma = self.dict_table.item(current_row, 0).text()
            return lemma + " "
        return ""

    def _check_existing_collocation(self, phrase: str) -> bool:
        """Проверяет существование словосочетания и увеличивает частоту."""
        existing = (
            self.db.get_session().query(Collocation).filter_by(phrase=phrase).first()
        )
        if existing:
            try:
                existing.frequency += 1
                self.db.get_session().commit()
                self.refresh_dictionary_table()

                current_row = self.dict_table.currentRow()
                if current_row >= 0:
                    lemma = self.dict_table.item(current_row, 0).text()
                    self.show_word_collocations_for_lemma(lemma)

                self.statusbar.showMessage(
                    f"Частота словосочетания '{phrase}' увеличена до {existing.frequency}"
                )
                QMessageBox.information(
                    self,
                    "Частота обновлена",
                    f"Словосочетание '{phrase}' уже существует.\n"
                    f"Частота увеличена до {existing.frequency}.",
                )
                return True
            except Exception as e:
                logger.exception("Ошибка при обновлении частоты: %s", e)
                QMessageBox.critical(self, "Ошибка", str(e))
                return True
        return False

    def _extract_meaningful_words(self, phrase: str) -> dict:
        """Извлекает значимые слова из фразы с помощью spaCy."""
        import spacy

        word_pos_map = {}
        valid_pos = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}

        try:
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(phrase)
            for token in doc:
                # Добавляем только значимые слова (не предлоги, артикли и т.д.)
                if token.pos_ in valid_pos and not token.is_stop and not token.is_punct:
                    word_pos_map[token.lemma_.lower()] = token.pos_
        except OSError:
            # Если spaCy не доступен, возвращаем пустой словарь
            pass

        return word_pos_map

    def _show_pos_selection_dialog(self, word: str, suggested_pos: str = None) -> str:
        """Показывает диалог для выбора части речи слова."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Выбор части речи: '{word}'")
        dialog.setMinimumWidth(300)

        layout = QFormLayout(dialog)

        # Информация о слове
        info_label = QLabel(f"Определите часть речи для слова '{word}':")
        layout.addRow(info_label)

        # Выпадающий список частей речи
        pos_combo = QComboBox()
        pos_options = ["NOUN", "VERB", "ADJ", "ADV", "PROPN"]
        pos_combo.addItems(pos_options)

        # Устанавливаем предложенную часть речи, если она есть и валидна
        if suggested_pos and suggested_pos in pos_options:
            pos_combo.setCurrentText(suggested_pos)
        layout.addRow("Часть речи:", pos_combo)

        # Кнопки
        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("Добавить")
        btn_cancel = QPushButton("Пропустить")
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        layout.addRow(buttons_layout)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return pos_combo.currentText()
        return None

    def _add_missing_words(self, phrase: str, word_pos_map: dict) -> list:
        """Добавляет отсутствующие слова в словарь с выбором части речи."""
        session = self.db.get_session()
        added_words = []

        # Получаем только значимые слова из фразы
        all_words = phrase.split()
        meaningful_words = [w for w in all_words if w in word_pos_map]

        for word_lemma in meaningful_words:
            existing_word = session.query(Word).filter_by(lemma=word_lemma).first()
            if not existing_word:
                # Получаем предложенную часть речи от spaCy
                suggested_pos = word_pos_map.get(word_lemma)

                # Показываем диалог для выбора части речи
                selected_pos = self._show_pos_selection_dialog(
                    word_lemma, suggested_pos
                )

                if selected_pos:  # Если пользователь не нажал "Пропустить"
                    self.db.add_word(word_lemma, selected_pos)
                    added_words.append((word_lemma, selected_pos))

        return added_words

    def _show_add_collocation_result(self, phrase: str, added_words: list):
        """Показывает результат добавления словосочетания."""
        self.statusbar.showMessage(f"Словосочетание '{phrase}' добавлено")
        logger.debug("Добавлено словосочетание: %s (частота: 1)", phrase)

        if added_words:
            words_info = "\n".join(
                [f"  {word} ({pos if pos else 'без ЧР'})" for word, pos in added_words]
            )
            QMessageBox.information(
                self,
                "Словосочетание добавлено",
                f"Словосочетание '{phrase}' добавлено.\n\n"
                f"Добавлены новые слова ({len(added_words)}):\n{words_info}",
            )
        else:
            QMessageBox.information(
                self,
                "Словосочетание добавлено",
                f"Словосочетание '{phrase}' добавлено.\n\n"
                f"Все слова уже существуют в словаре.",
            )

    def add_collocation_dialog(self):
        """Открывает диалог для добавления нового словосочетания."""
        # Создаем диалог
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить словосочетание")
        dialog.setMinimumWidth(400)

        layout = QFormLayout(dialog)

        # Поле ввода
        phrase_input = QLineEdit()
        phrase_input.setPlaceholderText("Введите словосочетание...")
        phrase_input.setText(self._get_default_phrase())
        layout.addRow("Словосочетание:", phrase_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("Добавить")
        btn_cancel = QPushButton("Отмена")
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        layout.addRow(buttons_layout)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        # Обработка результата
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        phrase = phrase_input.text().strip().lower()
        if not phrase:
            QMessageBox.warning(self, "Ошибка", "Введите словосочетание")
            return

        # Проверка на существование
        if self._check_existing_collocation(phrase):
            return

        # Получаем значимые слова
        word_pos_map = self._extract_meaningful_words(phrase)

        if not word_pos_map:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Не удалось определить значимые слова в словосочетании.\n"
                "Убедитесь, что словосочетание содержит существительные, "
                "глаголы, прилагательные или наречия.",
            )
            return

        try:
            # Добавляем отсутствующие слова
            added_words = self._add_missing_words(phrase, word_pos_map)

            # Добавляем словосочетание
            meaningful_word_list = list(word_pos_map.keys())
            self.db.add_collocation(phrase, meaningful_word_list, 1, None)

            # Обновляем UI
            self.refresh_dictionary_table()
            current_row = self.dict_table.currentRow()
            if current_row >= 0:
                lemma = self.dict_table.item(current_row, 0).text()
                self.show_word_collocations_for_lemma(lemma)

            # Показываем результат
            self._show_add_collocation_result(phrase, added_words)

        except Exception as e:
            logger.exception("Ошибка при добавлении словосочетания '%s': %s", phrase, e)
            QMessageBox.critical(
                self, "Ошибка", f"Ошибка при добавлении словосочетания:\n{str(e)}"
            )

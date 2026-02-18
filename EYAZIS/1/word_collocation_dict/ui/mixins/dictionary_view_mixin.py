"""Миксин для просмотра и фильтрации словаря."""

import logging

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QHeaderView,
    QMessageBox,
    QSpinBox,
    QWidget,
)

from ...database.models import Word

logger = logging.getLogger(__name__)


class DictionaryViewMixin:
    """Миксин для просмотра и фильтрации словаря."""

    def create_dictionary_tab(self) -> QWidget:
        """Создает вкладку для просмотра словаря."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Группа фильтров
        filter_group = QGroupBox("Фильтры")
        filter_layout = QHBoxLayout(filter_group)

        # Фильтр по тексту
        filter_layout.addWidget(QLabel("Поиск:"))
        self.text_filter = QLineEdit()
        self.text_filter.setPlaceholderText("Введите буквы для фильтрации...")
        self.text_filter.textChanged.connect(self.filter_dictionary_by_text)
        filter_layout.addWidget(self.text_filter)

        # Фильтр по части речи
        filter_layout.addWidget(QLabel("Часть речи:"))
        self.pos_filter = QComboBox()
        self.pos_filter.addItem("Все")
        self.pos_filter.addItems(["NOUN", "VERB", "ADJ", "ADV", "PROPN"])
        self.pos_filter.currentTextChanged.connect(self.refresh_dictionary_table)
        filter_layout.addWidget(self.pos_filter)

        # Фильтр по количеству словосочетаний
        filter_layout.addWidget(QLabel("Кол-во сочетаний:"))
        self.collocation_count_filter = QSpinBox()
        self.collocation_count_filter.setRange(-1, 9999)
        self.collocation_count_filter.setValue(-1)
        self.collocation_count_filter.setSpecialValueText("Любое")
        self.collocation_count_filter.valueChanged.connect(
            self.refresh_dictionary_table
        )
        filter_layout.addWidget(self.collocation_count_filter)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.clicked.connect(self.refresh_dictionary_table)
        filter_layout.addWidget(btn_refresh)
        layout.addWidget(filter_group)

        # Таблица словаря
        dict_table_layout = QVBoxLayout()
        dict_buttons_layout = QHBoxLayout()
        btn_add_word = QPushButton("Добавить слово")
        btn_add_word.clicked.connect(self.add_word_dialog)
        dict_buttons_layout.addWidget(btn_add_word)
        btn_delete_word = QPushButton("Удалить слово")
        btn_delete_word.clicked.connect(self.delete_selected_word)
        dict_buttons_layout.addWidget(btn_delete_word)
        dict_buttons_layout.addStretch()
        dict_table_layout.addLayout(dict_buttons_layout)

        self.dict_table = QTableWidget()
        self.dict_table.setColumnCount(3)
        self.dict_table.setHorizontalHeaderLabels(
            ["Слово (лемма)", "Часть речи", "Кол-во словосочетаний"]
        )
        self.dict_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.dict_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.dict_table.itemDoubleClicked.connect(self.show_word_collocations)
        self.dict_table.itemSelectionChanged.connect(self.on_word_selection_changed)
        self.dict_table.itemChanged.connect(self.on_word_item_changed)
        self.dict_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        dict_table_layout.addWidget(self.dict_table)
        layout.addLayout(dict_table_layout)

        # Словосочетания
        collocation_group = QGroupBox("Словосочетания для выбранного слова")
        collocation_layout = QVBoxLayout(collocation_group)
        collocation_buttons_layout = QHBoxLayout()
        btn_add_collocation = QPushButton("Добавить словосочетание")
        btn_add_collocation.clicked.connect(self.add_collocation_dialog)
        collocation_buttons_layout.addWidget(btn_add_collocation)
        btn_delete_collocation = QPushButton("Удалить словосочетание")
        btn_delete_collocation.clicked.connect(self.delete_selected_collocation)
        collocation_buttons_layout.addWidget(btn_delete_collocation)
        collocation_buttons_layout.addStretch()
        collocation_layout.addLayout(collocation_buttons_layout)
        self.collocation_table = QTableWidget()
        self.collocation_table.setColumnCount(2)
        self.collocation_table.setHorizontalHeaderLabels(["Словосочетание", "Частота"])
        self.collocation_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.collocation_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        collocation_layout.addWidget(self.collocation_table)
        layout.addWidget(collocation_group)
        return widget

    def refresh_dictionary_table(self):
        """Обновляет таблицу словаря с учетом всех фильтров."""
        pos_filter = self.pos_filter.currentText()
        text_filter = self.text_filter.text().strip().lower()
        collocation_count_filter = self.collocation_count_filter.value()

        logger.debug(
            "Обновление таблицы словаря: pos=%s, text=%s, count=%s",
            pos_filter,
            text_filter,
            collocation_count_filter,
        )

        try:
            # Получаем все слова
            words = self.db.get_all_words()

            # Фильтр по части речи
            if pos_filter != "Все":
                words = [w for w in words if w.pos == pos_filter]

            # Фильтр по тексту
            if text_filter:
                words = [w for w in words if w.lemma.lower().startswith(text_filter)]

            # Фильтр по количеству словосочетаний
            if collocation_count_filter >= 0:
                filtered_words = []
                for w in words:
                    collocs = self.db.get_word_collocations(w.lemma)
                    if len(collocs) == collocation_count_filter:
                        filtered_words.append(w)
                words = filtered_words

            logger.debug("Загружено слов для отображения: %d", len(words))
            self.dict_table.setRowCount(len(words))
            for i, word in enumerate(words):
                self.dict_table.setItem(i, 0, QTableWidgetItem(word.lemma))
                self.dict_table.setItem(i, 1, QTableWidgetItem(word.pos or ""))
                filtered_collocations = self.db.get_word_collocations(word.lemma)
                collocation_count = len(filtered_collocations)
                self.dict_table.setItem(i, 2, QTableWidgetItem(str(collocation_count)))
        except Exception as e:
            logger.exception("Ошибка при обновлении таблицы словаря: %s", e)
            raise

    def filter_dictionary_by_text(self):
        """Динамическая фильтрация словаря по введенному тексту."""
        self.refresh_dictionary_table()

    def show_word_collocations(self, item: QTableWidgetItem):
        """Показывает словосочетания для выбранного слова."""
        row = item.row()
        lemma = self.dict_table.item(row, 0).text()
        self.show_word_collocations_for_lemma(lemma)

    def on_word_selection_changed(self):
        """Обработчик изменения выбора слова в таблице."""
        current_row = self.dict_table.currentRow()
        if current_row >= 0:
            lemma = self.dict_table.item(current_row, 0).text()
            self.show_word_collocations_for_lemma(lemma)

    def show_word_collocations_for_lemma(self, lemma: str):
        """Показывает словосочетания для указанной леммы."""
        collocations = self.db.get_word_collocations(lemma)
        logger.debug(
            "Показать словосочетания для '%s': найдено %d", lemma, len(collocations)
        )
        self.collocation_table.setRowCount(len(collocations))
        for i, colloc in enumerate(collocations):
            self.collocation_table.setItem(i, 0, QTableWidgetItem(colloc.phrase))
            self.collocation_table.setItem(
                i, 1, QTableWidgetItem(str(colloc.frequency))
            )

    def on_word_item_changed(self, item: QTableWidgetItem):
        """Обработчик изменения элемента в таблице слов."""
        if item.column() == 0:  # Изменение леммы
            old_lemma = self.dict_table.item(item.row(), 0).text()
            new_lemma = item.text().strip()
            if new_lemma and new_lemma != old_lemma:
                session = self.db.get_session()
                try:
                    word = session.query(Word).filter_by(lemma=old_lemma).first()
                    if word:
                        existing = (
                            session.query(Word).filter_by(lemma=new_lemma).first()
                        )
                        if existing:
                            logger.warning(
                                "Попытка переименовать в существующее слово: %s",
                                new_lemma,
                            )
                            QMessageBox.warning(
                                self, "Ошибка", f"Слово '{new_lemma}' уже существует"
                            )
                            item.setText(old_lemma)
                        else:
                            word.lemma = new_lemma
                            session.commit()
                            self.statusbar.showMessage(f"Слово обновлено: {new_lemma}")
                except Exception as e:
                    logger.exception(
                        "Ошибка при обновлении леммы '%s' -> '%s': %s",
                        old_lemma,
                        new_lemma,
                        e,
                    )
                    QMessageBox.critical(
                        self, "Ошибка", f"Ошибка при обновлении:\n{str(e)}"
                    )
                    item.setText(old_lemma)
                finally:
                    session.close()
        elif item.column() == 1:  # Изменение части речи
            lemma = self.dict_table.item(item.row(), 0).text()
            new_pos = item.text().strip()
            session = self.db.get_session()
            try:
                word = session.query(Word).filter_by(lemma=lemma).first()
                if word:
                    word.pos = new_pos if new_pos else None
                    session.commit()
                    self.statusbar.showMessage(f"Часть речи обновлена для '{lemma}'")
            except Exception as e:
                logger.exception(
                    "Ошибка при обновлении части речи для '%s': %s", lemma, e
                )
                QMessageBox.critical(
                    self, "Ошибка", f"Ошибка при обновлении:\n{str(e)}"
                )
            finally:
                session.close()

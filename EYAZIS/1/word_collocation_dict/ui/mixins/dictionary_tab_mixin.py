"""Миксин для вкладки 'Словарь' (комбинированный)."""

from .dictionary_view_mixin import DictionaryViewMixin
from .dictionary_edit_mixin import DictionaryEditMixin


class DictionaryTabMixin(DictionaryViewMixin, DictionaryEditMixin):
    """Комбинированный миксин для работы с вкладкой словаря.

    Наследует функционал от:
    - DictionaryViewMixin: просмотр, фильтрация, отображение таблиц
    - DictionaryEditMixin: добавление, удаление слов и словосочетаний
    """

    pass

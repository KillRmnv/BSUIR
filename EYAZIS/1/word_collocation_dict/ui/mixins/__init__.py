"""Миксины для вкладок UI."""

from .file_tab_mixin import FileTabMixin
from .dictionary_view_mixin import DictionaryViewMixin
from .dictionary_edit_mixin import DictionaryEditMixin
from .synthesizer_tab_mixin import SynthesizerTabMixin
from .storage_mixin import StorageMixin

# Для обратной совместимости
from .dictionary_tab_mixin import DictionaryTabMixin

__all__ = [
    "FileTabMixin",
    "DictionaryViewMixin",
    "DictionaryEditMixin",
    "DictionaryTabMixin",
    "SynthesizerTabMixin",
    "StorageMixin",
]

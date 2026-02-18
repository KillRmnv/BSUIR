"""Модуль экспорта/импорта словаря."""
from .interfaces import IDictionaryExporter, IDictionaryImporter
from .factory import StorageFactory

__all__ = ['IDictionaryExporter', 'IDictionaryImporter', 'StorageFactory']

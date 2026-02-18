"""Фабрика для получения реализации экспорта/импорта по формату."""
from pathlib import Path
from typing import Optional

from .interfaces import IDictionaryExporter, IDictionaryImporter
from .exporters import TxtDictionaryExporter, CsvDictionaryExporter
from .importers import TxtDictionaryImporter, CsvDictionaryImporter


class StorageFactory:
    """Фабрика реализаций экспорта и импорта словаря."""
    
    _exporters: list[type[IDictionaryExporter]] = [
        TxtDictionaryExporter,
        CsvDictionaryExporter,
    ]
    _importers: list[type[IDictionaryImporter]] = [
        TxtDictionaryImporter,
        CsvDictionaryImporter,
    ]
    
    @classmethod
    def get_exporter(cls, path: Path) -> Optional[IDictionaryExporter]:
        """
        Возвращает реализацию экспорта для данного файла.
        
        Args:
            path: Путь к файлу (определяется по расширению)
            
        Returns:
            Экземпляр экспортера или None
        """
        ext = Path(path).suffix.lower()
        for exporter_cls in cls._exporters:
            inst = exporter_cls()
            if ext in inst.supported_extensions:
                return inst
        return None
    
    @classmethod
    def get_importer(cls, path: Path) -> Optional[IDictionaryImporter]:
        """
        Возвращает реализацию импорта для данного файла.
        
        Args:
            path: Путь к файлу
            
        Returns:
            Экземпляр импортера или None
        """
        ext = Path(path).suffix.lower()
        for importer_cls in cls._importers:
            inst = importer_cls()
            if ext in inst.supported_extensions:
                return inst
        return None
    
    @classmethod
    def get_supported_export_extensions(cls) -> list[str]:
        """Все поддерживаемые расширения для экспорта."""
        exts = set()
        for exporter_cls in cls._exporters:
            exts.update(exporter_cls().supported_extensions)
        return sorted(exts)
    
    @classmethod
    def get_supported_import_extensions(cls) -> list[str]:
        """Все поддерживаемые расширения для импорта."""
        exts = set()
        for importer_cls in cls._importers:
            exts.update(importer_cls().supported_extensions)
        return sorted(exts)

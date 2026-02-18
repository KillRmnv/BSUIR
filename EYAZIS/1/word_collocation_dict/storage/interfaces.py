"""Интерфейсы для экспорта и импорта словаря."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class IDictionaryExporter(ABC):
    """Интерфейс экспорта словаря в файл."""
    
    @abstractmethod
    def export(self, path: Path, data: Any) -> None:
        """
        Экспортирует данные словаря в файл.
        
        Args:
            path: Путь к файлу
            data: Данные для экспорта (список слов с словосочетаниями)
        """
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Поддерживаемые расширения файлов."""
        pass


class IDictionaryImporter(ABC):
    """Интерфейс импорта словаря из файла."""
    
    @abstractmethod
    def load(self, path: Path) -> Any:
        """
        Загружает данные словаря из файла.
        
        Args:
            path: Путь к файлу
            
        Returns:
            Данные словаря (список кортежей (lemma, pos, list[(phrase, frequency)]))
        """
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Поддерживаемые расширения файлов."""
        pass

"""Реализации экспорта словаря."""
import csv
from pathlib import Path
from typing import Any

from .interfaces import IDictionaryExporter


def words_to_export_data(words: Any, get_collocations_func=None) -> list:
    """
    Преобразует список Word в структуру для экспорта (lemma, pos, [(phrase, freq), ...]).
    get_collocations_func: опционально (lemma) -> list[Collocation], если у word нет загруженных collocations.
    """
    result = []
    for word in words:
        if hasattr(word, 'collocations') and word.collocations is not None:
            collocations = [
                (c.phrase, c.frequency)
                for c in word.collocations
                if word.lemma.lower() in c.phrase.lower().split()
            ]
        elif get_collocations_func:
            collocations = [(c.phrase, c.frequency) for c in get_collocations_func(word.lemma)]
        else:
            collocations = []
        result.append((word.lemma, word.pos or '', collocations))
    return result


class TxtDictionaryExporter(IDictionaryExporter):
    
    @property
    def supported_extensions(self) -> list[str]:
        return ['.txt', '.text']
    
    def export(self, path: Path, data: Any) -> None:
        path = Path(path)
        if data and hasattr(data[0], 'lemma'):
            data = words_to_export_data(data)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Словарь словосочетаний\n")
            f.write("=" * 50 + "\n\n")
            for lemma, pos, collocations in data:
                f.write(f"{lemma} ({pos or 'N/A'})\n")
                for phrase, freq in collocations:
                    f.write(f"  - {phrase} (частота: {freq})\n")
                f.write("\n")


class CsvDictionaryExporter(IDictionaryExporter):
    @property
    def supported_extensions(self) -> list[str]:
        return ['.csv']
    
    def export(self, path: Path, data: Any) -> None:
        path = Path(path)
        if data and hasattr(data[0], 'lemma'):
            data = words_to_export_data(data)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Лемма', 'Часть речи', 'Количество словосочетаний'])
            for lemma, pos, collocations in data:
                writer.writerow([lemma, pos or '', len(collocations)])

import csv
import re
from pathlib import Path
from typing import Any

from .interfaces import IDictionaryImporter


class TxtDictionaryImporter(IDictionaryImporter):
    
    @property
    def supported_extensions(self) -> list[str]:
        return ['.txt', '.text']
    
    def load(self, path: Path) -> list[tuple[str, str, list[tuple[str, int]]]]:
        path = Path(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        result = []
        current_lemma = None
        current_pos = None
        current_collocations = []
        
        for line in content.splitlines():
            line = line.rstrip()
            if not line:
                if current_lemma is not None:
                    result.append((current_lemma, current_pos or '', current_collocations))
                    current_lemma = current_pos = None
                    current_collocations = []
                continue
            
            if line.lstrip().startswith('- '):
                match = re.match(r'\s*-\s+(.+?)\s*\(\s*частота:\s*(\d+)\s*\)', line)
                if match:
                    phrase, freq = match.group(1).strip(), int(match.group(2))
                    current_collocations.append((phrase, freq))
                else:
                    phrase = line.lstrip()[2:].strip()
                    if phrase:
                        current_collocations.append((phrase, 1))
            elif not line.startswith('=') and 'Словарь' not in line:
                match = re.match(r'^(.+?)\s*\(\s*(.*?)\s*\)\s*$', line.strip())
                if match and not line.strip().startswith('-'):
                    word_part, pos_part = match.group(1).strip(), match.group(2).strip()
                    if pos_part.upper() in ('N/A', '') or len(pos_part) <= 10:
                        if current_lemma is not None:
                            result.append((current_lemma, current_pos or '', current_collocations))
                        current_lemma = word_part
                        current_pos = pos_part if pos_part != 'N/A' else ''
                        current_collocations = []
        
        if current_lemma is not None:
            result.append((current_lemma, current_pos or '', current_collocations))
        
        return result


class CsvDictionaryImporter(IDictionaryImporter):
    
    @property
    def supported_extensions(self) -> list[str]:
        return ['.csv']
    
    def load(self, path: Path) -> list[tuple[str, str, list[tuple[str, int]]]]:
        path = Path(path)
        result = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 1:
                    lemma = row[0].strip()
                    pos = row[1].strip() if len(row) > 1 else ''
                    result.append((lemma, pos, []))  
        return result

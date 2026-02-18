# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 4: Реализовать обратный нечёткий логический вывод на основе операции нечёткой композиции 
# (min({1}v{sum({max({0}v{xi+yi-1})|i})}))
#  Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А., Германенко В.В. 
#  Файл, содержащий класс для выделения фактов, матриц и обратных выводов из текста базы знаний

from typing import Dict, List, Tuple
from decimal import Decimal
import regex 
import grammar as g

FuzzySet = List[Tuple[str, Decimal]]
FactsDict = Dict[str, FuzzySet]
# Матрица правила - список строк, каждая строка - список чисел
Matrix = List[List[Decimal]]
MatricesDict = Dict[str, Matrix]
# Обратный вывод: (имя_вывода, имя_множества, имя_матрицы, результирующее_множество)
ReverseInference = Tuple[str, str, str, FuzzySet]
ReverseInferenceList = List[ReverseInference]

class FuzzyKBParser:
    def __init__(self):
        self.validator = g.GrammarValidator()
        self.facts: FactsDict = {}
        self.matrices: MatricesDict = {}
        self.reverse_inferences: ReverseInferenceList = []
        self.eps: Decimal = Decimal('0.001')  # значение по умолчанию

    def parse_line(self, line: str):
        line = line.strip()
        if not line:
            return

        if self.validator.check_grammar(line, "<факт>"):
            self._parse_fact(line)

        elif self.validator.check_grammar(line, "<точность>"):
            pass

        elif self.validator.check_grammar(line, "<погрешность>"):
            self._parse_eps(line)


    def _parse_fact(self, line: str):
        """Разбор факта, матрицы или обратного вывода с использованием grammar.py"""
        # Сначала пробуем разобрать как обратный вывод по регулярке <обратный вывод>
        if self.validator.check_grammar(line, "<обратный вывод>"):
            self._parse_reverse_inference(line)
            return
        
        # Затем как матрицу правила по регулярке <матрица правила>
        if self.validator.check_grammar(line, "<матрица правила>"):
            self._parse_matrix(line)
            return
        
    def _extract_pairs(self, fact_name: str, set_str: str):

        pairs: List[Tuple[str, Decimal]] = []
        existing_elements = set()

        # Восстанавливаем фигурные скобки, чтобы работать с полным множеством
        full_set_str = "{" + set_str + "}"

        pair_pattern = regex.compile(
            r'<\s*([^,<>]+?)\s*,\s*([0-9](?:\.[0-9]+)?|1\.0+)\s*>'
        )
        raw_pairs = pair_pattern.findall(full_set_str)

        for elem_name, degree_str in raw_pairs:
                elem_name = elem_name.strip()
                degree_str = degree_str.strip()

                degree = Decimal(degree_str)

                if elem_name in existing_elements:
                    return None

                pairs.append((elem_name, degree))
                existing_elements.add(elem_name)

        return pairs

    def _parse_eps(self, line: str):
        """Разбор строки с погрешностью: eps=0.001"""       
        _, eps_str = line.split('=', 1)
        eps_str = eps_str.strip()
        
        eps_value = Decimal(eps_str)    
        self.eps = eps_value


    def _parse_matrix(self, line: str):
        """Разбор матрицы правила: A=(0.6 0.3 0.2; 0.5 0.4 0.3)"""
        name, matrix_str = line.split('=', 1)
        name = name.strip()
        matrix_str = matrix_str.strip()
        
        # Отрезаем первую '(' и последнюю ')'
        inner = matrix_str.lstrip()[1:]
        # удаляем последнюю ')' (и возможные пробелы/переводы строк перед ней)
        last_paren = inner.rfind(')')
        if last_paren != -1:
            inner = inner[:last_paren]

        # Делим по строкам; каждая непустая строка — строка матрицы
        raw_rows = [r.strip() for r in inner.splitlines() if r.strip()]
        
        matrix: Matrix = []
        for row_str in raw_rows:
            # элементы разделены пробелами
            elems = row_str.split()
            row: List[Decimal] = []
            for elem in elems:
                val = Decimal(elem)
                row.append(val)
            if row:
                matrix.append(row)
        
        if matrix:
            # Проверяем, что все строки имеют одинаковую длину
            row_len = len(matrix[0])
            if any(len(row) != row_len for row in matrix):
                return
            
            if name in self.matrices:
                return
            
            self.matrices[name] = matrix
    
    def _parse_reverse_inference(self, line: str):
        """Разбор обратного вывода: I1=B(x)/~\A = {<a,0.2>,<b,0.9>,<c,1.0>}"""
      
        first_eq = line.find('=')
        if first_eq == -1:
            return
        
        inference_name = line[:first_eq].strip()
        rest = line[first_eq+1:].strip()
        
        # Разделяем на часть до '=' (B(x)/~A) и часть после '=' ({...})
        if '=' not in rest:
            return
        
        left_part, set_str = rest.split('=', 1)
        left_part = left_part.strip()
        set_str = set_str.strip()
        
        # Разбираем левую часть: B(x)/~\A (структура гарантирована грамматикой)
        if '/~\\' not in left_part:
            return
        
        set_name_part, matrix_name = left_part.split('/~\\', 1)
        set_name_part = set_name_part.strip()
        matrix_name = matrix_name.strip()
        
        # Извлекаем имя множества из B(x)
        if '(' in set_name_part and set_name_part.endswith(')'):
            set_name = set_name_part.split('(')[0].strip()
        else:
            set_name = set_name_part.strip()
        
        # Разбираем множество справа.
        # На этом этапе мы доверяем грамматике <обратный вывод>, но дополнительно проверяем фигурные скобки.
        if not (set_str.startswith('{') and set_str.endswith('}')):
            return
        
        inner_set = set_str[1:-1].strip()
        pairs = self._extract_pairs(inference_name, inner_set)
        
        if pairs:
            self.reverse_inferences.append((inference_name, set_name, matrix_name, pairs))

    def parse_text(self, kb_text: str):
        self.facts.clear()
        self.matrices.clear()
        self.reverse_inferences.clear()
        self.eps = Decimal('0.001')  # сброс к значению по умолчанию

        lines = kb_text.splitlines()
        i = 0
        n = len(lines)

        while i < n:
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # Начало объявления матрицы правила вида "A=("
            if "=(" in stripped and not stripped.endswith(")"):
                block_lines = [line]
                i += 1
                # Собираем строки до строки с ')'
                while i < n:
                    block_lines.append(lines[i])
                    if lines[i].strip().endswith(")"):
                        break
                    i += 1

                block_text = "\n".join(block_lines)
                self.parse_line(block_text)
                i += 1
                continue

            # Обычная строка
            self.parse_line(line)
            i += 1

        return self.facts, self.matrices, self.reverse_inferences, self.eps

#  Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем 
#  Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
#  и нечеткую импликацию Лукасевича. 
#  Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А., Германенко В.В. 
#  Файл, содержащий класс для выделения фактов и правил из текста базы знаний 
#  Дата выполнения: 30.10.2025

from typing import Dict, List, Tuple
import grammar as g

FuzzySet = List[Tuple[str, float]]
FactsDict = Dict[str, FuzzySet]
RulesList = List[Tuple[str, str]]

class FuzzyKBParser:
    def __init__(self):
        self.validator = g.GrammarValidator()
        self.facts: FactsDict = {}
        self.rules: RulesList = []

    def parse_line(self, line: str):
        line = line.strip()
        if not line:
            return

        if self.validator.check_grammar(line, "<факт>"):
            self._parse_fact(line)

        elif self.validator.check_grammar(line, "<правило>"):
            self._parse_rule(line)

        elif self.validator.check_grammar(line, "<точность>"):
            pass

        else:
            print(f"Некорректная строка пропущена: {line}")


    # --------------------------
    # Вспомогательные методы
    # --------------------------

    def _parse_fact(self, line: str):
        """Разбор факта"""
        name, set_str = line.split('=', 1)
        name = name.strip()

        if name in self.facts:
            print(f"Факт '{name}' уже определён ранее — повторное определение пропущено.")
            return

        # Убираем фигурные скобки { ... }
        set_str = set_str.strip()
        if not (set_str.startswith('{') and set_str.endswith('}')):
            print(f"Ошибка синтаксиса в факте '{name}' — отсутствуют фигурные скобки.")
            return

        set_str = set_str[1:-1].strip()
        pairs = self._extract_pairs(name, set_str)

        if pairs:
            self.facts[name] = pairs


    def _extract_pairs(self, fact_name: str, set_str: str):
        """Извлекает пары <элемент, значение> из строки факта"""
        pairs = []
        existing_elements = set()
        i = 0
        valid = True

        while i < len(set_str):
            if set_str[i] == '<':
                j = set_str.find('>', i)
                if j == -1:
                    print(f"Ошибка синтаксиса в факте '{fact_name}' — пропущен '>'")
                    valid = False
                    break

                pair_str = set_str[i + 1:j]
                if ',' not in pair_str:
                    print(f"Ошибка в паре '{pair_str}' в факте '{fact_name}' — пропущена запятая")
                    valid = False
                    break

                elem_name, degree_str = pair_str.split(',', 1)
                elem_name = elem_name.strip()
                degree_str = degree_str.strip()

                if not self._is_float(degree_str):
                    print(f"Ошибка: степень принадлежности '{degree_str}' в факте '{fact_name}' не является числом.")
                    valid = False
                    break

                degree = float(degree_str)

                if elem_name in existing_elements:
                    print(f"Повторяющийся элемент '{elem_name}' в факте '{fact_name}' — факт пропущен.")
                    valid = False
                    break

                pairs.append((elem_name, degree))
                existing_elements.add(elem_name)
                i = j + 1
            else:
                i += 1

        return pairs if valid else None


    def _is_float(self, value: str) -> bool:
        """Проверяет, можно ли преобразовать строку в float """
        if not value:
            return False
        digits = value.replace('.', '', 1)
        return digits.isdigit() or (digits.startswith('-') and digits[1:].replace('.', '', 1).isdigit())


    def _parse_rule(self, line: str):
        """Разбор правила"""
        if '~>' not in line:
            print(f"Ошибка в правиле: отсутствует '~>' — строка '{line}' пропущена.")
            return
        from_name, to_name = line.split('~>', 1)
        self.rules.append((from_name.strip(), to_name.strip()))



    def parse_text(self, kb_text: str):
        self.facts.clear()
        self.rules.clear()
        for line in kb_text.splitlines():
            self.parse_line(line)
        return self.facts, self.rules

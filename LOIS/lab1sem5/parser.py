# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий функции для выделения фактов и правил из текста базы знаний
# Дата выполнения: 19.10.2025


import re
import grammar
from typing import Dict, List, Tuple

FuzzySet = List[Tuple[str, float]]
FactsDict = Dict[str, FuzzySet]
RulesList = List[Tuple[str, str]]

def parse_fuzzy_kb(kb_text: str) -> Tuple[FactsDict, RulesList]:
    facts_dict: FactsDict = {}
    rules_list: RulesList = []

    # Факты
    fact_pattern = re.compile(grammar.GRAMMAR["<факт>"])
    pair_pattern = re.compile(grammar.GRAMMAR["<пара нечёткой принадлежности>"])

    for fact_match in fact_pattern.finditer(kb_text):
        fact_str = fact_match.group()
        name, fuzzy_set_str = fact_str.split('=', 1)
        name = name.strip()

        fuzzy_set_str = fuzzy_set_str.strip()[1:-1]

        pairs: FuzzySet = []
        for pair_match in pair_pattern.finditer(fuzzy_set_str):
            pair_str = pair_match.group()[1:-1] 
            elem, degree = pair_str.split(',')
            pairs.append((elem.strip(), float(degree.strip())))

        facts_dict[name] = pairs

    rule_pattern = re.compile(grammar.GRAMMAR["<правило>"])
    for rule_match in rule_pattern.finditer(kb_text):
        rule_str = rule_match.group()
        from_set, to_set = rule_str.split('~>')
        to_set = to_set.replace('.', '')  # убираем точку
        rules_list.append((from_set.strip(), to_set.strip()))

    return facts_dict, rules_list

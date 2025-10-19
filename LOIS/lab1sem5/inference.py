# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий функции реализующие прямой логический вывод,треугольную норму пограничного произведения,импликацию Лукасевича
# Дата выполнения: 19.10.2025

from typing import Dict, List, Tuple

FuzzySet = List[Tuple[str, float]]  
FactsDict = Dict[str, FuzzySet]
RulesList = List[Tuple[str, str]]

def t_norm(a: float, b: float) -> float:
    return max(0.0, a + b - 1.0)

def imp(a: float, b: float) -> float:
    return min(1.0, 1.0 - a + b)

def find_sets(sample_set: FuzzySet, facts: FactsDict) -> Dict[str, FuzzySet]:
    sample_names = {elem for elem, _ in sample_set}
    results = {}
    for name, fset in facts.items():
        fset_names = {elem for elem, _ in fset}
        if fset_names == sample_names:
            results[name] = fset
    return results

def fuzzy_inference(facts: FactsDict, rules: RulesList) -> FactsDict:
    new_facts = facts.copy()
    infer_counter = 1
    updated = True

    while updated:
        updated = False
        additions: Dict[str, FuzzySet] = {}

        for from_name, to_name in rules:
            if from_name not in new_facts or to_name not in new_facts:
                continue

            from_set = new_facts[from_name]
            to_set = new_facts[to_name]

            matching_sets = find_sets(from_set, new_facts)

            for match_name, match_set in matching_sets.items():
                result_dict = {}
                for elem_to, deg_to in to_set:
                    max_val = 0.0
                    for elem, deg in from_set:
                        imp_val = imp(deg, deg_to)
                        for el, deg_match in match_set:
                            if el == elem:
                                t_val = t_norm(deg_match, imp_val)
                                break
                        max_val = max(max_val, t_val)
                    result_dict[elem_to] = max_val

                new_list = [(elem, round(max(result_dict.get(elem, 0.0), deg), 2)) for elem, deg in to_set]

                if new_list != to_set and new_list not in new_facts.values() and new_list not in additions.values():
                    if match_name.find('=')!=-1:
                        match_name,other_part=match_name.split('=')
                    new_name = rf"I{infer_counter}={match_name}/~\{{{from_name}~>{to_name}}}"

                    infer_counter += 1
                    additions[new_name] = new_list
                    updated = True

        new_facts.update(additions)

    return new_facts

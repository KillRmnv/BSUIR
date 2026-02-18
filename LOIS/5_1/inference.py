# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий класс реализующий прямой логический вывод,треугольную норму пограничного произведения,импликацию Лукасевича
# Дата выполнения: 30.10.2025
from typing import Dict, List, Tuple
from decimal import Decimal, getcontext

# Настройка глобальной точности
getcontext().prec = 10

FuzzySet = List[Tuple[str, float]]  
FactsDict = Dict[str, FuzzySet]
RulesList = List[Tuple[str, str]]

class FuzzyInferenceEngine:
    """
    Класс для выполнения прямого нечёткого логического вывода
    с использованием треугольной нормы граничного произведения и импликации Лукасевича
    """
    def __init__(self, facts: FactsDict, rules: RulesList):
        # Преобразуем все значения в Decimal
        self.facts: FactsDict = {name: [(e, Decimal(str(d))) for e,d in fset] for name,fset in facts.items()}
        self.rules: RulesList = rules.copy()
        self.infer_counter: int = 1
        self.applied_rules:Dict[str,set[Tuple[str, str]]]={}
        self.equal_sets:Dict[str,str]={}

    @staticmethod
    def t_norm(a: Decimal, b: Decimal) -> Decimal:
        """Треугольная норма граничного произведения"""
        return max(Decimal(0), a + b - Decimal(1))
    def get_equals(self):
        return self.equal_sets
    @staticmethod
    def imp(a: Decimal, b: Decimal) -> Decimal:
        """Нечёткая импликация Лукасевича"""
        return min(Decimal(1), Decimal(1) - a + b)

    def find_sets(self, sample_set: FuzzySet, facts: FactsDict, from_name: str, to_name: str) -> Dict[str, FuzzySet]:
        """Находит факты с совпадающими элементами множества"""
        sample_names = {elem for elem, _ in sample_set}
        results = {}
        rule_key = (from_name, to_name)

        for name, fset in facts.items():
            fset_names = {elem for elem, _ in fset}

            if name not in self.applied_rules:
                self.applied_rules[name] = set()


            if (fset_names == sample_names
                and rule_key not in self.applied_rules[name]
                and name not in self.equal_sets):  

                results[name] = fset
                self.applied_rules[name].add(rule_key)


        return results
    def infer(self) -> FactsDict:
        """Выполняет прямой нечёткий вывод по всем правилам"""
        while True:
            additions = self._process_rules()
            if not additions:
                break
            self.facts.update(additions['facts'])
            self.infer_counter = additions['infer_counter']
        return {name: [(e, float(d)) for e,d in fset] for name,fset in self.facts.items()}

    def _process_rules(self) -> Dict:
        additions = {}
        current_infer_counter = self.infer_counter
        add=False
        rule_additions={}
        for from_name, to_name in self.rules:
            if not self._can_apply_rule(from_name, to_name):
                continue
            rule_additions = self._apply_single_rule(from_name, to_name, current_infer_counter,add)
            additions.update(rule_additions['facts'])
            current_infer_counter = rule_additions['infer_counter']

        if not  rule_additions.get('add'):
            return {}
        return {'facts': additions, 'infer_counter': current_infer_counter}

    def _can_apply_rule(self, from_name: str, to_name: str) -> bool:
        return from_name.split('(',1)[0] in self.facts and to_name.split('(',1)[0] in self.facts

    def _apply_single_rule(self, from_name: str, to_name: str, infer_counter: int,add:bool) -> Dict:
        from_set = self.facts[from_name.split('(',1)[0]]
        to_set = self.facts[to_name.split('(',1)[0]]
        matching_sets = self.find_sets(from_set, self.facts,from_name,to_name)
        additions = {}
        current_infer_counter = infer_counter

        for match_name, match_set in matching_sets.items():
            new_fuzzy_set = self._compute_new_fuzzy_set(from_set, to_set, match_set)
            new_name = self._generate_fact_name(match_name, from_name, to_name, current_infer_counter)

            current_infer_counter += 1
            if self._should_add_new_fact(new_fuzzy_set, to_set, additions,new_name):
                add=True

        return {'facts': additions, 'infer_counter': current_infer_counter,'add':add} 

    def _compute_new_fuzzy_set(self, from_set: FuzzySet, to_set: FuzzySet, match_set: FuzzySet) -> FuzzySet:
        """Вычисляет новое нечёткое множество с выводом матрицы импликации"""


        result_dict = {}
        for elem_to, deg_to in to_set:
            deg_to_dec = Decimal(str(deg_to))
            max_val = Decimal(0)
            for elem, deg in from_set:
                deg_dec = Decimal(str(deg))
                imp_val = self.imp(deg_dec, deg_to_dec)
                match_deg = self._find_matching_degree(elem, match_set)
                t_val = self.t_norm(match_deg, imp_val)
                max_val = max(max_val, t_val)
            result_dict[elem_to] = max_val
        return [(elem, result_dict.get(elem, Decimal(0))) for elem, _ in to_set]


    @staticmethod
    def _find_matching_degree(elem: str, match_set: FuzzySet) -> Decimal:
        for el, deg_match in match_set:
            if el == elem:
                return Decimal(str(deg_match))
        return Decimal(0)

    def _should_add_new_fact(self, new_set: FuzzySet, original_set: FuzzySet, additions: Dict,new_name:str) -> bool:
        """
        Проверяет, нужно ли добавлять новое нечёткое множество как факт:
        - Оно отличается от оригинального множества,
        - Ещё не существует среди текущих фактов (без учёта порядка элементов),
        - Ещё не добавлено в текущую итерацию.
        """
        new_set_as_set = set(new_set)
        additions[new_name] = new_set
        #comment this to remove dublicates
        for name,fset in additions.items():
            if new_set_as_set == set(fset) and not name==new_name:
                self.equal_sets[new_name]=name
                return False
                
        #additions[new_name] = new_set
        # uncomment this it to remove dublicates
        for name,fset in self.facts.items():
            if new_set_as_set == set(fset):
                self.equal_sets[new_name]=name
                return False



        return True


    @staticmethod
    def _generate_fact_name(match_name: str, from_name: str, to_name: str, infer_counter: int) -> str:
        if '=' in match_name:
            match_name, _ = match_name.split('=')
        return f"I{infer_counter}={match_name}/~\{{{from_name}~>{to_name}}}"

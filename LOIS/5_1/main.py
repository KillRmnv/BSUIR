# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий класс для чтения данных с тестовых файлов,записи результатов в текстовые файлы
# Дата выполнения: 30.10.2025

from typing import List
from parser import FuzzyKBParser
from inference import FuzzyInferenceEngine
from grammar import GrammarValidator
import re
class FuzzyKBProcessor:
    """Класс для чтения файлов, парсинга, вывода и записи результатов"""
    def __init__(self, file_list: List[str]):
        self.files = file_list
        self.parser = FuzzyKBParser()
        self.precision = 5
        self.validator = GrammarValidator()

    def correct_format_of_set(self, pairs) -> str:
        """Форматирует нечёткое множество для вывода"""
        result = '{'
        for elem, deg in pairs:
            result += f'<{elem},{round(deg, self.precision)}>,'
        if result=='{':
            return '{'+'}'
        return result[:-1] + '}'
    def correct_format_of_set_without_rounding(self, pairs) -> str:
        """Форматирует нечёткое множество для вывода"""
        result = '{'
        for elem, deg in pairs:
            result += f'<{elem},{deg}>,'
        if result=='{':
            return '{'+'}'
        return result[:-1] + '}'
    @staticmethod
    def read_file(file_name: str) -> str:
        f = open(file_name, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        return content

    def print_implication_matrix(self, from_set, to_set, from_name, to_name):
            """Выводит таблицу импликации Лукасевича для from_name(x) → to_name(y)"""
            print(f"\nМатрица импликации для {from_name}(x) → {to_name}(y)")
            print("I_L = min(1, 1 - a + b):")

            header = "           " + "".join([f"{y:^10}" for y, _ in to_set])
            print(header)
            print("-" * len(header))

            for x, a_val in from_set:
                row = f"{x:<10}"
                for _, b_val in to_set:
                    val = min(1.0, 1.0 - float(a_val) + float(b_val))
                    row += f"{val:^10.3f}"
                print(row)
            print()

    def write_file(self, file_name: str, facts: dict,engine:FuzzyInferenceEngine):
            """Записывает результат в файл и выводит на экран"""
            name, ext = file_name.split('.')
            out_file = f"{name}_result.{ext}"

            f = open(out_file, 'w', encoding='utf-8')
            for fact_name, pairs in facts.items():
                
                additon:str=engine.get_equals().get(fact_name)
                if additon:
                    if additon.find('='):
                        additon=additon.split('=',1)[0]
                    print(f"{fact_name} = {self.correct_format_of_set(pairs)}={additon}")
                    f.write(f"{fact_name} = {self.correct_format_of_set_without_rounding(pairs)}={additon}\n")
                else:
                    print(f"{fact_name} = {self.correct_format_of_set(pairs)}")
                    f.write(f"{fact_name} = {self.correct_format_of_set_without_rounding(pairs)}\n")
                # all_predicates=self.validator.find_all_elements(fact_name,"<имя нечёткого предиката>")
                # if len(all_predicates)>1:
                #     left_name =  all_predicates[0][0]
                #     right_name = all_predicates[1][0]
                #     if left_name in facts and right_name in facts:
                #         self.print_implication_matrix(facts[left_name], facts[right_name], left_name, right_name)

            f.close()


    def process_files(self):
        """Обрабатывает все файлы из списка"""
        for file_name in self.files:
            print(f"\nProcessing file: {file_name}\n{'-' * 40}")
            kb_text = self.read_file(file_name)
            self.precision = self.validator.get_precision(kb_text)

            facts_dict, rules_list = self.parser.parse_text(kb_text)
            engine = FuzzyInferenceEngine(facts_dict, rules_list)
            inferred_facts = engine.infer()

            self.write_file(file_name, inferred_facts,engine)

if __name__ == "__main__":
    files = ["test1.txt", "test2.txt", "test3.txt","test4.txt"]
    #files = [ "test3.txt"]

    processor = FuzzyKBProcessor(files)
    processor.process_files()
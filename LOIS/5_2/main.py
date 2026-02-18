# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 4: Реализовать обратный нечёткий логический вывод на основе операции нечёткой композиции 
# (min({1}v{sum({max({0}v{xi+yi-1})|i})}))
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий класс для чтения данных с тестовых файлов, записи результатов в текстовые файлы

from typing import List
from parser import FuzzyKBParser
from inference import FuzzyInferenceEngine
from grammar import GrammarValidator
class FuzzyKBProcessor:
    """Класс для чтения файлов, парсинга, вывода и записи результатов"""
    def __init__(self, file_list: List[str]):
        self.files = file_list
        self.parser = FuzzyKBParser()
        self.precision = 5
        self.validator = GrammarValidator()

    def correct_format_of_set(self, pairs) -> str:
        """Форматирует нечёткое множество для вывода"""
        from decimal import Decimal
        result = '{'
        for elem, deg in pairs:
            if isinstance(deg, Decimal):
                result += f'<{elem},{round(deg, self.precision)}>,'
            else:
                result += f'<{elem},{round(float(deg), self.precision)}>,'
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
    
    def correct_format_of_bounds(self, bounds) -> str:
        """Форматирует границы обратного вывода для вывода"""
        from decimal import Decimal
        result = '{'
        for elem, (lower, upper) in bounds:
            if isinstance(lower, Decimal) and isinstance(upper, Decimal):
                result += f'<{elem},[{round(lower, self.precision)},{round(upper, self.precision)}]>,'
            else:
                result += f'<{elem},[{round(float(lower), self.precision)},{round(float(upper), self.precision)}]>,'
        if result=='{':
            return '{'+'}'
        return result[:-1] + '}'
    
    def correct_format_of_bounds_without_rounding(self, bounds) -> str:
        """Форматирует границы обратного вывода для вывода без округления"""
        result = '{'
        for elem, (lower, upper) in bounds:
            result += f'<{elem},[{lower},{upper}]>,'
        if result=='{':
            return '{'+'}'
        return result[:-1] + '}'
    
    def format_union_of_intervals(self, bounds_list) -> str:
        """Форматирует список решений как объединение промежутков в формате декартова произведения"""
        from decimal import Decimal
        
        if not bounds_list:
            return "{}"
        
        # Извлекаем bounds из списка (может быть tuple (name, bounds) или просто bounds)
        solutions = []
        for item in bounds_list:
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
                _, bounds = item
            else:
                bounds = item
            solutions.append(bounds)
        
        # Форматируем каждое решение как декартово произведение промежутков
        formatted_solutions = []
        for bounds in solutions:
            intervals = []
            for elem, (lower, upper) in bounds:
                # Форматируем интервал [lower;upper] с точкой с запятой
                interval_str = f"[{lower};{upper}]"
                intervals.append(interval_str)
            
            # Объединяем интервалы через X (декартово произведение)
            cartesian_product = " X ".join(intervals)
            formatted_solutions.append(f"({cartesian_product})")
        
        # Объединяем все решения через ∪
        return " \n∪ ".join(formatted_solutions)
    
    @staticmethod
    def read_file(file_name: str) -> str:
        f = open(file_name, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        return content

    def write_file(self, file_name: str, facts: dict,engine:FuzzyInferenceEngine):
            """Записывает результат в файл и выводит на экран"""
            name, ext = file_name.split('.')
            out_file = f"{name}_result.{ext}"

            f = open(out_file, 'w', encoding='utf-8')
            reverse_inf_list = engine.get_reverse_inferences()
            reverse_set_names = {inf[1] for inf in reverse_inf_list}
            
            for fact_name, pairs in facts.items():
                # Пропускаем факты, которые являются результатами обратного вывода
                # (они имеют вид B1, B2, B3... где B - имя множества из обратного вывода)
                is_reverse_result = False
                for set_name in reverse_set_names:
                    if fact_name.startswith(set_name) and fact_name[len(set_name):].isdigit():
                        is_reverse_result = True
                        break
                if is_reverse_result:
                    continue
                    
                print(f"{fact_name} = {self.correct_format_of_set(pairs)}")
                f.write(f"{fact_name} = {self.correct_format_of_set_without_rounding(pairs)}\n")
            
            # Выводим результаты обратного вывода как объединение промежутков
            reverse_inf_list = engine.get_reverse_inferences()
            
            # Создаём маппинг: inference_name -> set_name
            inference_to_set = {inf[0]: inf[1] for inf in reverse_inf_list}
            
            # Получаем результаты обратного вывода (список дизъюнктных областей)
            reverse_results = engine.get_reverse_results()
            
            for inference_name, bounds_list in reverse_results.items():
                set_name = inference_to_set.get(inference_name, inference_name)
                
                if not bounds_list:
                    # Если решений нет, выводим пустое множество
                    print(f"{set_name} = {{}}")
                    f.write(f"{set_name} = {{}}\n")
                else:
                    # Выводим объединение промежутков в формате декартова произведения
                    union_format = self.format_union_of_intervals(bounds_list)
                    print(f"{set_name} = {union_format}")
                    f.write(f"{set_name} = {union_format}\n")

            f.close()


    def process_files(self):
        """Обрабатывает все файлы из списка"""
        for file_name in self.files:
            print(f"\nProcessing file: {file_name}\n{'-' * 40}")
            kb_text = self.read_file(file_name)
            self.precision = self.validator.get_precision(kb_text)

            facts_dict, matrices_dict, reverse_inferences, eps = self.parser.parse_text(kb_text)
            engine = FuzzyInferenceEngine(facts_dict, matrices_dict, reverse_inferences, eps)
            inferred_facts = engine.infer()

            self.write_file(file_name, inferred_facts,engine)

if __name__ == "__main__":
    files = ["test1.txt", "test2.txt","test4.txt","test5.txt"]
    
    processor = FuzzyKBProcessor(files)
    processor.process_files()
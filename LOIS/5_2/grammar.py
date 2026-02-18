# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 4: Реализовать обратный нечёткий логический вывод на основе операции нечёткой композиции 
# (min({1}v{sum({max({0}v{xi+yi-1})|i})}))
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий класс для проверки корректности формата базы знаний
import regex
class GrammarValidator:
    GRAMMAR = {}
    def __init__(self):
            self.GRAMMAR["<цифра>"] = r'[0-9]'
            self.GRAMMAR["<буква>"] = r'[A-Za-z]'
            self.GRAMMAR["<символ>"] = rf'({self.GRAMMAR["<буква>"]}|{self.GRAMMAR["<цифра>"]})'
            self.GRAMMAR["<имя>"] = rf'({self.GRAMMAR["<буква>"]}|({self.GRAMMAR["<буква>"]}{self.GRAMMAR["<символ>"]}*))'
            self.GRAMMAR["<имя нечёткого множества>"] = self.GRAMMAR["<имя>"]
            self.GRAMMAR["<имя нечёткого предиката>"] = rf'{self.GRAMMAR["<имя>"]}\({self.GRAMMAR["<имя>"]}\)'
            self.GRAMMAR["<единица>"] = r'1\.0+'
            self.GRAMMAR["<действительное число с 0 до 1>"] = rf'0(\.[0-9]*)?'
            self.GRAMMAR["<действительное число с 0 по 1>"] = rf'({self.GRAMMAR["<единица>"]}|{self.GRAMMAR["<действительное число с 0 до 1>"]})'
            self.GRAMMAR["<степень принадлежности>"] = self.GRAMMAR["<действительное число с 0 по 1>"]
            self.GRAMMAR["<элемент>"] = self.GRAMMAR["<имя>"]
            self.GRAMMAR["<список элементов>"] = rf'{self.GRAMMAR["<элемент>"]}(,{self.GRAMMAR["<элемент>"]})*'

            self.GRAMMAR["<пара нечёткой принадлежности>"] = rf'<\s*{self.GRAMMAR["<элемент>"]}\s*,\s*{self.GRAMMAR["<степень принадлежности>"]}\s*>'
            self.GRAMMAR["<список пар нечёткой принадлежности>"] = rf'\s*{self.GRAMMAR["<пара нечёткой принадлежности>"]}\s*(,\s*{self.GRAMMAR["<пара нечёткой принадлежности>"]}\s*)*'
            self.GRAMMAR["<нечёткое множество>"] = rf'\{{({self.GRAMMAR["<список пар нечёткой принадлежности>"]})?\}}'
            
            self.GRAMMAR["<элемент матрицы>"] = self.GRAMMAR["<действительное число с 0 по 1>"]
            self.GRAMMAR["<строка матрицы>"] = rf'{self.GRAMMAR["<элемент матрицы>"]}(\s+{self.GRAMMAR["<элемент матрицы>"]})*'
            self.GRAMMAR["<матрица>"] = rf'\s*\(\s*{self.GRAMMAR["<строка матрицы>"]}(\s*\n\s*{self.GRAMMAR["<строка матрицы>"]})+\s*\)'
            self.GRAMMAR["<матрица правила>"] = rf'{self.GRAMMAR["<имя>"]}\s*=\s*{self.GRAMMAR["<матрица>"]}'
            
            self.GRAMMAR["<обратный вывод>"] = rf'{self.GRAMMAR["<имя>"]}\s*=\s*{self.GRAMMAR["<имя>"]}\({self.GRAMMAR["<имя>"]}\)\s*/\~\\\s*{self.GRAMMAR["<имя>"]}\s*=\s*{self.GRAMMAR["<нечёткое множество>"]}'
            
            self.GRAMMAR["<факт>"] = rf'({self.GRAMMAR["<имя нечёткого множества>"]}\s*=\s*{self.GRAMMAR["<нечёткое множество>"]}|{self.GRAMMAR["<матрица правила>"]}|{self.GRAMMAR["<обратный вывод>"]})'
            self.GRAMMAR["<список фактов>"] = rf'{self.GRAMMAR["<факт>"]}(?:\s*\n+\s*{self.GRAMMAR["<факт>"]})*'
            self.GRAMMAR["<база знаний>"] = (rf'{self.GRAMMAR["<список фактов>"]}\s*$')
            self.GRAMMAR["<точность>"]=rf'precision\s?=\s?\d+'
            self.GRAMMAR["<погрешность>"]=rf'eps\s?=\s?{self.GRAMMAR["<действительное число с 0 по 1>"]}'
    def get_grammar(self)->dict:
        return self.GRAMMAR

    def check_grammar(self,kb,el)->bool:
        pattern = regex.compile(self.GRAMMAR[el])
        return pattern.match(kb) 
    def find_all_elements(self,kb,el)->list:
        pattern=regex.compile(self.GRAMMAR[el])
        return pattern.findall(kb)
    def get_precision(self, kb) -> int:
        pattern = regex.compile(self.GRAMMAR["<точность>"])
        match = pattern.search(kb)
        if match:
            value = match.group().split('=')[1].strip()
            if int (value)>1:
                return int(value)
        return 5 
        
# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий функцию для проверки корректности формата базы знаний 
# Дата выполнения: 19.10.2025
import regex

GRAMMAR = {}

GRAMMAR["<цифра>"] = r'[0-9]'
GRAMMAR["<буква>"] = r'[A-Za-z]'
GRAMMAR["<символ>"] = rf'({GRAMMAR["<буква>"]}|{GRAMMAR["<цифра>"]})'
GRAMMAR["<имя>"] = rf'({GRAMMAR["<буква>"]}|({GRAMMAR["<буква>"]}{GRAMMAR["<символ>"]}*))'
GRAMMAR["<имя нечёткого множества>"] = GRAMMAR["<имя>"]
GRAMMAR["<имя нечёткого предиката>"] = rf'{GRAMMAR["<имя>"]}\({GRAMMAR["<имя>"]}\)'
GRAMMAR["<единица>"] = r'1\.0+'
GRAMMAR["<действительное число с 0 до 1>"] = rf'0(\.[0-9]*)?'
GRAMMAR["<действительное число с 0 по 1>"] = rf'({GRAMMAR["<единица>"]}|{GRAMMAR["<действительное число с 0 до 1>"]})'
GRAMMAR["<степень принадлежности>"] = GRAMMAR["<действительное число с 0 по 1>"]
GRAMMAR["<элемент>"] = GRAMMAR["<имя>"]
GRAMMAR["<список элементов>"] = rf'{GRAMMAR["<элемент>"]}(,{GRAMMAR["<элемент>"]})*'


GRAMMAR["<список>"]=rf'{GRAMMAR["<имя>"]}(,{GRAMMAR["<имя>"]})*'
GRAMMAR["<неориентированное множество>"] = rf'\{{(?:{GRAMMAR["<список>"]}(,(?R))|(?R))*\}}'
GRAMMAR["<ориентированное множество>"] = rf'\{{(?:<{GRAMMAR["<неориентированное множество>"]}(,{GRAMMAR["<неориентированное множество>"]})*>|(?(DEFINE)(?R))(?R))*\}}'
GRAMMAR["<множество>"] = rf'({GRAMMAR["<ориентированное множество>"]}|{GRAMMAR["<неориентированное множество>"]})'

GRAMMAR["<пара нечёткой принадлежности>"] = rf'<{GRAMMAR["<элемент>"]},\s*{GRAMMAR["<степень принадлежности>"]}>'
GRAMMAR["<список пар нечёткой принадлежности>"] = rf'{GRAMMAR["<пара нечёткой принадлежности>"]}(,\s*{GRAMMAR["<пара нечёткой принадлежности>"]})+'
GRAMMAR["<нечёткое множество>"] = rf'\{{({GRAMMAR["<список пар нечёткой принадлежности>"]})?\}}'
GRAMMAR["<факт>"] = rf'{GRAMMAR["<имя нечёткого предиката>"]}\s*=\s*{GRAMMAR["<нечёткое множество>"]}'
GRAMMAR["<правило>"] = rf'{GRAMMAR["<имя нечёткого предиката>"]}\s*~>\s*{GRAMMAR["<имя нечёткого предиката>"]}'
GRAMMAR["<список фактов>"] = rf'{GRAMMAR["<факт>"]}(?:\s*\n+\s*{GRAMMAR["<факт>"]})*'
GRAMMAR["<список правил>"] = rf'{GRAMMAR["<правило>"]}(?:\s*\n+\s*{GRAMMAR["<правило>"]})*'
GRAMMAR["<база знаний>"] = (rf'{GRAMMAR["<список фактов>"]}(?:\s*\n+\s*{GRAMMAR["<список правил>"]})?\s*$')



def check_grammar_full(kb: str) -> bool:
    kb = kb.strip()
    all_passed = True
    results = {}

    for key, pattern_str in GRAMMAR.items():
        pattern = regex.compile(pattern_str, regex.MULTILINE)
        full_match = pattern.fullmatch(kb)
        results[key] = {"full": bool(full_match)}
        
        if not full_match:
            all_passed = False
            partial_matches = list(pattern.finditer(kb))
            results[key]["partial"] = [m.group() for m in partial_matches] if partial_matches else []

    for key, value in results.items():
        print(f"{key}: совпадения={value.get('partial', [])}")

    return all_passed

def check_grammar(kb)->bool:
    pattern = regex.compile(GRAMMAR["<база знаний>"])
    if(pattern.match(kb)):
        return True
    check_grammar_full(kb)
    return False
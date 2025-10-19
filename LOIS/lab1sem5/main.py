# Лабораторная работа №1 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Реализовать прямой нечёткий логический вывод, используя треугольную норму граничного произведения 
# и нечеткую импликацию Лукасевича.
# Выполнили студенты группы 321701: Романов К.В., Рапчинский В.А.,Германенко В.В.
# Файл, содержащий функции для чтения данных с тестовых файлов,записи результатов в текстовые файлы
# Дата выполнения: 19.10.2025
import grammar
import parser
import inference
def main():
    files = ["test1.txt", "test2.txt", "test3.txt"] 
    for file_name in files:
        print(f"file: {file_name}\n")
        if(not grammar.check_grammar(read_file(file_name))):
            print(f"Некорректная грамматика в файле:{file_name}")
            continue
        facts_dict, rules_list=parser.parse_fuzzy_kb(read_file(file_name))
        facts_dict=inference.fuzzy_inference(facts_dict,rules_list) 
        write_file(file_name,facts_dict)   
        
    return 0
def correct_format_of_set(pairs)->str:
    result='{'
    for pair in pairs:
        result+='<'+str(pair[0])+','+str(pair[1])+'>,'
    return result[:-1]+'}'
def read_file(file_name):
    with open(file_name, 'r') as file:
            return file.read()
def write_file(file_name:str,facts):
    file_name,file_extension=file_name.split('.')
    with open(f"{file_name}_result.{file_extension}", "w", encoding="utf-8") as f:
        for name, pairs in facts.items():
            f.write(f"{name} = {correct_format_of_set(pairs)}\n")
            print(f"{name} = {correct_format_of_set(pairs)}\n")
            
if __name__=="__main__":
   main()
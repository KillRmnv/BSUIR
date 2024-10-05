#include "UI.h"
using namespace sets;
void UI::menu()
{
	input forsets;
	do {
		forsets.string_input();
	} while (!forsets.sets(this->num_1));
	std::cout << this->num_1; std::cout << std::endl;
	do {
		forsets.string_input();
	} while (!forsets.sets(this->num_2));
	std::cout << this->num_2; std::cout << std::endl;
	set result; int choice = 1; std::string input;
	do {
		do {
			if (std::cin.fail() || choice < 1 || choice>10) {
				std::cin.clear();
				std::cin.ignore(10000, '\n');
			}
			std::cout << "1.проверка на пустое множество" << std::endl << "2.добавление элемента" << std::endl << "3.удаление элемента" << std::endl << "4.определение мощности множества" << std::endl << "5.проверка принадлежности элемента множеству" << std::endl << "6.объединение двух множеств" << std::endl << "7.пересечение двух множеств" << std::endl << "8.разность двух множеств" << std::endl << "9.построение булеана данного множества" << std::endl << "10. Завершить" << std::endl;
			std::cin >> choice;
		} while (std::cin.fail() || choice < 1 || choice>10);
		switch (choice) {
		case 1:
			if (this->num_1.check_on_emptiness())
				std::cout << "Множество 1 пустое" << std::endl;
			else
				std::cout << "Множество 1 не пустое" << std::endl;
			if (this->num_2.check_on_emptiness())
				std::cout << "Множество 2 пустое" << std::endl;
			else
				std::cout << "Множество 2 не пустое" << std::endl;
			break;
		case 2:
			std::cin.ignore();
			do {
				forsets.string_input(); result.~set(); result = this->num_1;
			} while (!forsets.sets(result));
			this->num_1 = result;
			std::cout << this->num_1; std::cout << std::endl;
			do {
				forsets.string_input(); result.~set(); result = this->num_2;
			} while (!forsets.sets(result));  this->num_2 = result; result.~set();
			std::cout << this->num_2; std::cout << std::endl;
			break;
		case 3:
			std::cin.ignore();
			if (!this->num_1.check_on_emptiness()) {
				this->num_1.del_element(forsets); std::cout << this->num_1;
			}
			else
				std::cout << "Множество 1 пустое" << std::endl;
			if (!this->num_2.check_on_emptiness()) {
				this->num_2.del_element(forsets); std::cout << this->num_2;
			}
			else
				std::cout << "Множество 2 пустое" << std::endl;
			break;
		case 4:
			std::cout << "Множество 1:" << this->num_1.amnt_of_elements() << std::endl;
			std::cout << std::endl << "Множество 2:" << this->num_2.amnt_of_elements() << std::endl;
			break;
		case 5:
			if (this->num_1.check_on_emptiness() != true) {
				std::cin.ignore();
				std::cout << "Введите строку:";
				std::getline(std::cin, input);
				if (this->num_1[input] != -1)
					std::cout << "Элемент " << input << " присутствует во множестве 1" << std::endl;
				else
					std::cout << "Элемент " << input << " отсутствует во множестве 1" << std::endl;;
			}
			else
				std::cout << "Не принадлежит" << std::endl;
			if (this->num_2.check_on_emptiness() != true) {
				std::cin.ignore();
				std::cout << std::endl << "Введите строку:";
				std::getline(std::cin, input);
				if (this->num_2[input] != -1)
					std::cout << "Элемент " << input << " присутствует во множестве 2" << std::endl;
				else
					std::cout << "Элемент " << input << " отсутствует во множестве 2" << std::endl;
			}
			else
				std::cout << "Не принадлежит" << std::endl;
			break;
		case 6:
			result = this->num_1 + this->num_2; std::cout << result; result.~set();
			std::cout << std::endl;
			break;
		case 7:
			result = this->num_1 * this->num_2; std::cout << result; result.~set();
			std::cout << std::endl;
			break;
		case 8:
			result = this->num_1 - this->num_2; std::cout << result << std::endl;  result.~set();
			result = this->num_2 - this->num_1; std::cout << result << std::endl;  result.~set();
			break;
		case 9:
			result = this->num_1;
			result.PowerSet();
			std::cout << result << std::endl; result.~set();
			result = this->num_2;
			result.PowerSet();
			std::cout << result << std::endl; result.~set();
			break;
		case 10:
			return;
		}
	} while (true);
}
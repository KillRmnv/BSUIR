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
			std::cout << "1.�������� �� ������ ���������" << std::endl << "2.���������� ��������" << std::endl << "3.�������� ��������" << std::endl << "4.����������� �������� ���������" << std::endl << "5.�������� �������������� �������� ���������" << std::endl << "6.����������� ���� ��������" << std::endl << "7.����������� ���� ��������" << std::endl << "8.�������� ���� ��������" << std::endl << "9.���������� ������� ������� ���������" << std::endl << "10. ���������" << std::endl;
			std::cin >> choice;
		} while (std::cin.fail() || choice < 1 || choice>10);
		switch (choice) {
		case 1:
			if (this->num_1.check_on_emptiness())
				std::cout << "��������� 1 ������" << std::endl;
			else
				std::cout << "��������� 1 �� ������" << std::endl;
			if (this->num_2.check_on_emptiness())
				std::cout << "��������� 2 ������" << std::endl;
			else
				std::cout << "��������� 2 �� ������" << std::endl;
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
				std::cout << "��������� 1 ������" << std::endl;
			if (!this->num_2.check_on_emptiness()) {
				this->num_2.del_element(forsets); std::cout << this->num_2;
			}
			else
				std::cout << "��������� 2 ������" << std::endl;
			break;
		case 4:
			std::cout << "��������� 1:" << this->num_1.amnt_of_elements() << std::endl;
			std::cout << std::endl << "��������� 2:" << this->num_2.amnt_of_elements() << std::endl;
			break;
		case 5:
			if (this->num_1.check_on_emptiness() != true) {
				std::cin.ignore();
				std::cout << "������� ������:";
				std::getline(std::cin, input);
				if (this->num_1[input] != -1)
					std::cout << "������� " << input << " ������������ �� ��������� 1" << std::endl;
				else
					std::cout << "������� " << input << " ����������� �� ��������� 1" << std::endl;;
			}
			else
				std::cout << "�� �����������" << std::endl;
			if (this->num_2.check_on_emptiness() != true) {
				std::cin.ignore();
				std::cout << std::endl << "������� ������:";
				std::getline(std::cin, input);
				if (this->num_2[input] != -1)
					std::cout << "������� " << input << " ������������ �� ��������� 2" << std::endl;
				else
					std::cout << "������� " << input << " ����������� �� ��������� 2" << std::endl;
			}
			else
				std::cout << "�� �����������" << std::endl;
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
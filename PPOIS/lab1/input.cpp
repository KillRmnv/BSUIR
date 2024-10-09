#include"input.h"
using namespace sets_ns;
std::string Input_set::string_input()&
{
	std::cout << std::endl << "¬ведите строку:";
	std::getline(std::cin, this->line);
	return del_all_space(this->line);
}
std::string Input_set::char_input()& {
	char line[256];
	std::cout << std::endl << "¬ведите строку:";
	std::cin.getline(line, 256);
	this->line = line;
	return del_all_space(this->line);
}
bool Input_set::Create_set(Set& num_1)
{
	if (!num_1.check_on_input(this->line))
		return false;
	if (this->line != "{}") {
		num_1.parsing(this->line);
		if (!num_1.check_on_repeats())
			return false;
	}
	return true;
}
std::string Input_set::getter()
{
	return this->line;
}
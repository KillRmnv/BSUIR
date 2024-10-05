#include <string>
#include<vector>
#include<iostream>
#include <algorithm>
#include <regex>
#include "lib.h"
namespace sets {
	sets::set::set() {}
	std::vector<element> sets::set::getter()
	{
		return this->Set;
	}
	std::string sets::element::elmnt()
	{
		return this->Element;
	}
	set* sets::element::Sub()
	{
		return this->Subset;
	}
	std::string sets::input::getter()
	{
		return this->line;
	}
	sets::set::set(const set& to_copy) {
		element hollow; hollow.fill("");
		for (size_t i = 0; i < to_copy.Set.size(); ++i)
			this->add_element(subset(const_cast<sets::element&>(to_copy.Set[i])));
	}
	element element::fill(const std::string& Element) {
		if (Element[0] == '{') {
			if (Element[1] == '}') {
				this->Element = "{}";
				return *this;
			}
			this->Subset = new set;
			this->Subset->parsing(Element);
		}
		else
			this->Element = Element;
		return *this;
	}
	bool element::compare_string(const element& a, const element& b) {
		return a.Element < b.Element;
	}
	void set::sort_descending() {
		std::sort(this->Set.begin(), this->Set.end(), element::compare_string);
	}
	bool sets::element::operator==(const element& anthr_element) const
	{
		if (this->Element == anthr_element.Element && this->Element != "")
			return true;
		else
			if (*this->Subset == anthr_element.Subset && this->Element == anthr_element.Element) {
				return true;
			}
			else
				if (this->Element == anthr_element.Element && this->Subset == nullptr && anthr_element.Subset == nullptr)
					return true;
		return false;
	}
	bool set::operator ==(const set* anthr_set) {
		if (anthr_set == nullptr || this == nullptr)
			return false;
		if (anthr_set->Set.size() == 0 && this->Set.size() == 0)
			return true;
		bool proof = false;
		if (this->Set.size() != anthr_set->Set.size()) {
			return false;
		}
		for (size_t i = 0; i < this->Set.size(); ++i) {
			proof = false;
			for (size_t j = 0; j < anthr_set->Set.size(); ++j) {
				if (this->Set[i] == anthr_set->Set[j]) {
					proof = true;
					break;
				}
			}
			if (proof == false)
				return false;
		}
		return true;
	}
	bool sets::set::operator!=(const set* anthr_set) {
		if (this->Set == anthr_set->Set)
			return false;
		return true;
	}
	std::string sets::Set(set* some_set)
	{
		std::string line = "{";
		for (size_t i = 0; i < some_set->getter().size() - 1; ++i) {
			line += subset(some_set->getter()[i]);
			line += ",";
		}
		line += subset(some_set->getter()[some_set->getter().size() - 1]);
		line += "}";
		return line;
	}
	std::string sets::subset(element& subst)
	{
		if (subst.Sub() != nullptr)
			return Set(subst.Sub());
		else
			return subst.elmnt();
	}
	void set::add_element(const std::string& Element) {
		element NewElement;
		NewElement.fill(Element);
		this->Set.push_back(NewElement);
	}
	bool set::check_on_input(const std::string& input) {
		int skb = 0;
		std::regex check_sequence(R"((\}\{)|(\{\s*,)|(,\s*\})|(,,)|(([a-zA-Z0-9]|\d)\{)|(\}([a-zA-Z0-9]|\d))|(\}\s+[a-zA-Z0-9])|(([a-zA-Z0-9]|\d)\s+\{))", std::regex_constants::ECMAScript);
		if (input.empty()) {
			return false;
		}
		if (input[input.size() - 1] != '}' || input[0] != '{')
			return false;
		skb++;
		for (int i = 1; i < input.size(); i++) {
			if (input[i] == '}') {
				skb--;
				if (skb == 0 && i != input.size() - 1) {
					return false;
				}
			}
			else if (input[i] == '{') {
				skb++;
			}
				if (std::regex_search(input, check_sequence))
					return false;
		}
		if (skb != 0)
			return false;
		return true;
	}
	int sets::set::amnt_of_elements()
	{
		element hollow; hollow.fill("");
		if (this->Set.size() == 1 && this->Set[0] == hollow)
			return 0;
		else
			return this->Set.size();
	}
	bool sets::set::check_on_emptiness()
	{
		if (this->amnt_of_elements() == 0)
			return true;
		return false;
	}
	void set::parsing(const std::string& input) {
		int ind = 0, counter = 0, amnt_of_staples = 0; element hollow;
		for (size_t i = 1; i < input.size(); ++i) {
			if (input[i] == '{') {
				ind = i; counter = 1; amnt_of_staples = 1;
				for (i++; amnt_of_staples != 0; i++ && counter++) {
					if (input[i] == '{') {
						amnt_of_staples++;
					}
					else
						if (input[i] == '}') {
							amnt_of_staples--;
						}
				}
				this->add_element(input.substr(ind, counter));
			}
			else
				if (input[i] != '{' && input[i] != '}' && input[i] != ',') {
					ind = i; counter = 1;
					for (; i < input.size() && input[i] != '{' && input[i] != '}' && input[i] != ','; counter++ && ++i); counter--;
					this->add_element(input.substr(ind, counter));
				}
				else
					if (i < input.length() - 1)i++;
		}
		this->sort_descending();
	}
	bool sets::set::check_on_repeats() {
		for (size_t i = 0; i < this->Set.size() - 1; ++i) {
			for (size_t j = i + 1; j < this->Set.size(); ++j) {
				if (this->Set[i] == this->Set[j])
					return false;
			}
		}
		return true;
	}
	std::string sets::del_all_space(std::string& input)
	{
		bool inword = false;  int ind1 = 0; int ind2 = 0; int skb = 0;
		for (size_t i = 0; i < input.length(); ++i) {
			if ((input[i] == '{' || input[i] == ',') && inword == true) {
				inword = false;
			}
			else {
				if (input[i] != ' ' && input[i] != ',' && input[i] != '{' && input[i] != '}') {
					inword = true;
				}
			}
			if (inword == false && input[i] == ' ') {
				for (ind1 = 0; input[i] == ' '; i++ && ind1++);
				input.erase(i - ind1, ind1);
				i = i - ind1;
			}
			else if (input[i] == ' ' && inword == true) {
				for (ind1 = 0; input[i + 1] == ' '; i++ && ind1++);
				input.erase(i - ind1, ind1);
				i = i - ind1;
			}
			if (input[i] == ' ' && (input[i + 1] == ',' || input[i + 1] == '}')) {
				input.erase(i, 1);
				i += -2;
			}
		}
		if (input[input.length() - 1] == ' ')
			input.erase(input.length() - 1, 1);
		if (input[0] == ' ')
			input.erase(0, 1);
		return input;
	}
	std::ostream& sets::operator<<(std::ostream& out, set& a)
	{
		out << "{";
		if (a.amnt_of_elements() != 0) {
			for (size_t i = 0; i < a.amnt_of_elements() - 1; ++i) {
				out << subset(a.getter()[i]) << ",";
			}
			out << subset(a.getter()[a.amnt_of_elements() - 1]);
		}
		out << "}";
		return out;
	}
	void sets::element::del_subset()
	{
		this->Subset->~set();
	}
	void set::PowerSet() {
		set powerSet;
		int n = this->Set.size(); element hollow;
		int totalSubsets = 1 << n; std::string line;
		for (int i = 0; i < totalSubsets; ++i) {
			line += "{";
			for (int j = 0; j < n; ++j) {
				if (i & (1 << j)) {
					line += subset(this->Set[j]); line += ",";
				}
			}
			if (line[line.length() - 1] == ',')
				line.erase(line.length() - 1, 1);
			line += "}";
			hollow.fill(line);
			powerSet.Set.push_back(hollow);
			line = "";
		}
		this->Set = powerSet.Set;
	}

	int sets::set::operator [](std::string& elmnt)
	{
		elmnt = del_all_space(elmnt); std::string line = "{"; line += elmnt; line += "}";
		set newel;	newel.parsing(line); int ind;
		for (ind = 0; !(this->Set[ind] == newel.Set[0]) && ind < this->Set.size() - 1; ++ind);
		if (this->Set[ind] == newel.Set[0])
			return ind;
		return -1;
	}
	void sets::set::del_element(input elmnt_to_del)
	{
		int buff; std::string line;
		do {
			elmnt_to_del.string_input(); line = elmnt_to_del.getter();
			buff = (*this)[line];
		} while (buff == -1);
		this->Set.erase(this->Set.begin() + buff);
	}
	set sets::set::operation_for_inter(const set& num_1, const set& num_2)
	{
		set newset; int ind = 0, size1 = num_1.Set.size(), size2 = num_2.Set.size();
		for (size_t i = 0; i < size1; ++i) {
			for (ind = 0; ind < size2; ++ind)
				if (num_1.Set[i] == num_2.Set[ind]) {
					newset.Set.push_back(this->Set[i]); break;
				}
		}
		newset.sort_descending();
		return newset;
	}
	set sets::set::operator*(const set& anthr_set)//пересечение
	{
		return this->operation_for_inter(*this, anthr_set);
	}
	set sets::set::operator*=(const set& anthr_set)
	{
		return this->operation_for_inter(*this, anthr_set);
	}
	set sets::set::operation_for_merge(set& num_1, const set& num_2)
	{
		int ind = 0, size = num_1.Set.size();
		for (size_t i = 0; i < num_2.Set.size(); ++i) {
			for (ind = 0; ind < size; ++ind) {
				if (num_1.Set[ind] == num_2.Set[i])
					break;
			}
			if (ind == size)
				num_1.Set.push_back(num_2.Set[i]);
		}
		num_1.sort_descending();
		return num_1;
	}
	set sets::set::operator+(const set& anthr_set)
	{
		return this->operation_for_merge(*this, anthr_set);
	}
	set sets::set::operator+=(const set& anthr_set)
	{
		return this->operation_for_merge(*this, anthr_set);
	}
	set sets::set::operation_for_diff(const set& num_1, const set& num_2)
	{
		set newset = num_1; int ind = 0, size2 = newset.Set.size(), size1 = num_2.Set.size();
		for (size_t i = 0; i < size1; ++i) {
			for (ind = 0; ind < size2; ++ind) {
				if (newset.Set[ind] == num_2.Set[i]) {
					newset.Set.erase(newset.Set.begin() + ind); size2--;
					break;
				}
			}
		}
		newset.sort_descending();
		return newset;
	}
	set sets::set::operator-(const set& anthr_set)
	{
		return this->operation_for_diff(*this, anthr_set);
	}
	set sets::set::operator-=(const set& anthr_set)
	{
		return this->operation_for_diff(*this, anthr_set);
	}
	sets::set::~set()
	{
		if (this == nullptr)
			return;
		element hollow; hollow.fill("");
		for (size_t i = 0; i < this->Set.size(); i++) {
			if (this->Set[i] == hollow)
				this->Set[i].del_subset();
		}
		this->Set.clear();
	}
	std::string sets::input::string_input()&
	{
		std::cout << std::endl << "Введите строку:";
		std::getline(std::cin, this->line);
		return del_all_space(this->line);
	}
	std::string sets::input::char_input()& {
		char line[256];
		std::cout << std::endl << "Введите строку:";
		std::cin.getline(line, 256);
		this->line = line;
		return del_all_space(this->line);
	}
	bool sets::input::sets(set& num_1)
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
}
#include <string>
#include<vector>
#include<iostream>
#include <algorithm>
#include <regex>
#include"input.h"
const std::regex check_sequence(R"((\}\{)|(\{\s*,)|(,\s*\})|(,,)|(([a-zA-Z0-9]|\d)\{)|(\}([a-zA-Z0-9]|\d))|(\}\s+[a-zA-Z0-9])|(([a-zA-Z0-9]|\d)\s+\{))", std::regex_constants::ECMAScript);
using namespace sets_ns;
	sets_ns::Set::Set() {}
	std::vector<Element> sets_ns::Set::getter()
	{
		return this->set;
	}
	
	sets_ns::Set::Set(const Set& to_copy) {
		Element hollow; hollow.fill("");
		for (size_t i = 0; i < to_copy.set.size(); ++i)
			this->add_element(subset(const_cast<sets_ns::Element&>(to_copy.set[i])));
	}
	void Set::sort_descending() {
		std::sort(this->set.begin(), this->set.end(), Element::compare_string);
	}
	bool Set::operator ==(const Set* anthr_set) {
		if (anthr_set == nullptr || this == nullptr)
			return false;
		if (anthr_set->set.size() == 0 && this->set.size() == 0)
			return true;
		bool proof = false;
		if (this->set.size() != anthr_set->set.size()) {
			return false;
		}
		for (size_t i = 0; i < this->set.size(); ++i) {
			proof = false;
			for (size_t j = 0; j < anthr_set->set.size(); ++j) {
				if (this->set[i] == anthr_set->set[j]) {
					proof = true;
					break;
				}
			}
			if (proof == false)
				return false;
		}
		return true;
	}
	bool sets_ns::Set::operator!=(const Set* anthr_set) {
		if (this->set == anthr_set->set)
			return false;
		return true;
	}
	std::string sets_ns::Sett(Set* some_set)
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
	std::string sets_ns::subset(Element& subst)
	{
		if (subst.Sub() != nullptr)
			return Sett(subst.Sub());
		else
			return subst.elmnt();
	}
	void Set::add_element(const std::string& element) {
		Element NewElement;
		NewElement.fill(element);
		this->set.push_back(NewElement);
	}
	bool Set::check_on_input(const std::string& input) {
		int skb = 0;
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
	int sets_ns::Set::amnt_of_elements()
	{
		Element hollow; hollow.fill("");
		if (this->set.size() == 1 && this->set[0] == hollow)
			return 0;
		else
			return this->set.size();
	}
	bool sets_ns::Set::check_on_emptiness()
	{
		if (this->amnt_of_elements() == 0)
			return true;
		return false;
	}
	void Set::parsing(const std::string& input) {
		int ind = 0, counter = 0, amnt_of_staples = 0; Element hollow;
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
	bool sets_ns::Set::check_on_repeats() {
		for (size_t i = 0; i < this->set.size() - 1; ++i) {
			for (size_t j = i + 1; j < this->set.size(); ++j) {
				if (this->set[i] == this->set[j])
					return false;
			}
		}
		return true;
	}
	std::string sets_ns::del_all_space(std::string& input)
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
	std::ostream& sets_ns::operator<<(std::ostream& out, Set& a)
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
	void Set::PowerSet() {
		Set powerSet;
		int n = this->set.size(); Element hollow;
		int totalSubsets = 1 << n; std::string line;
		for (int i = 0; i < totalSubsets; ++i) {
			line += "{";
			for (int j = 0; j < n; ++j) {
				if (i & (1 << j)) {
					line += subset(this->set[j]); line += ",";
				}
			}
			if (line[line.length() - 1] == ',')
				line.erase(line.length() - 1, 1);
			line += "}";
			hollow.fill(line);
			powerSet.set.push_back(hollow);
			line = "";
		}
		this->set = powerSet.set;
	}

	int sets_ns::Set::operator [](std::string& elmnt)
	{
		elmnt = del_all_space(elmnt); std::string line = "{"; line += elmnt; line += "}";
		Set newel;	newel.parsing(line); int ind;
		for (ind = 0; !(this->set[ind] == newel.set[0]) && ind < this->set.size() - 1; ++ind);
		if (this->set[ind] == newel.set[0])
			return ind;
		return -1;
	}
	void sets_ns::Set::del_element(Input_set elmnt_to_del)
	{
		int buff; std::string line;
		do {
			elmnt_to_del.string_input(); line = elmnt_to_del.getter();
			buff = (*this)[line];
		} while (buff == -1);
		this->set.erase(this->set.begin() + buff);
	}
	Set sets_ns::Set::operation_for_inter(const Set& num_1, const Set& num_2)
	{
		Set newset; int ind = 0, size1 = num_1.set.size(), size2 = num_2.set.size();
		for (size_t i = 0; i < size1; ++i) {
			for (ind = 0; ind < size2; ++ind)
				if (num_1.set[i] == num_2.set[ind]) {
					newset.set.push_back(this->set[i]); break;
				}
		}
		newset.sort_descending();
		return newset;
	}
	Set sets_ns::Set::operator*(const Set& anthr_set)
	{
		return this->operation_for_inter(*this, anthr_set);
	}
	Set sets_ns::Set::operator*=(const Set& anthr_set)
	{
		return this->operation_for_inter(*this, anthr_set);
	}
	Set sets_ns::Set::operation_for_merge(Set& num_1, const Set& num_2)
	{
		int ind = 0, size = num_1.set.size();
		for (size_t i = 0; i < num_2.set.size(); ++i) {
			for (ind = 0; ind < size; ++ind) {
				if (num_1.set[ind] == num_2.set[i])
					break;
			}
			if (ind == size)
				num_1.set.push_back(num_2.set[i]);
		}
		num_1.sort_descending();
		return num_1;
	}
	Set sets_ns::Set::operator+(const Set& anthr_set)
	{
		return this->operation_for_merge(*this, anthr_set);
	}
	Set sets_ns::Set::operator+=(const Set& anthr_set)
	{
		return this->operation_for_merge(*this, anthr_set);
	}
	Set sets_ns::Set::operation_for_diff(const Set& num_1, const Set& num_2)
	{
		Set newset = num_1; int ind = 0, size2 = newset.set.size(), size1 = num_2.set.size();
		for (size_t i = 0; i < size1; ++i) {
			for (ind = 0; ind < size2; ++ind) {
				if (newset.set[ind] == num_2.set[i]) {
					newset.set.erase(newset.set.begin() + ind); size2--;
					break;
				}
			}
		}
		newset.sort_descending();
		return newset;
	}
	Set sets_ns::Set::operator-(const Set& anthr_set)
	{
		return this->operation_for_diff(*this, anthr_set);
	}
	Set sets_ns::Set::operator-=(const Set& anthr_set)
	{
		return this->operation_for_diff(*this, anthr_set);
	}
	sets_ns::Set::~Set()
	{
		if (this == nullptr)
			return;
		Element hollow; hollow.fill("");
		for (size_t i = 0; i < this->set.size(); i++) {
			if (this->set[i] == hollow)
				this->set[i].del_subset();
		}
		this->set.clear();
	}

#pragma once
#include <string>
#include<vector>
#include<iostream>
namespace sets_ns {
	class Input_set;
	class Element;
	class Set {
	private:
		std::vector<Element> set;
		void add_element(const std::string& element);
		void sort_descending();
		Set operation_for_merge(Set& num_1, const Set& num_2);
		Set operation_for_inter(const Set& num_1, const Set& num_2);
		Set operation_for_diff(const Set& num_1, const Set& num_2);
	public:
		Set();
		Set(const Set& to_copy);
		std::vector<Element> getter();
		~Set();
		bool check_on_input(const std::string& input);
		bool check_on_repeats();
		void parsing(const std::string& input);
		bool operator ==(const Set* anthr_set);
		bool operator !=(const Set* anthr_set);
		bool check_on_emptiness();
		void del_element(Input_set elmnt_to_del);
		int  amnt_of_elements();
		Set operator +(const Set& anthr_set);
		Set operator +=(const Set& anthr_set);
		Set operator *(const Set& anthr_set);
		Set operator *=(const Set& anthr_set);
		int operator [](std::string& elmnt);
		Set operator -(const Set& anthr_set);
		Set operator -=(const Set& anthr_set);
		void PowerSet();
	};
	std::string del_all_space(std::string& input);
	std::ostream& operator<<(std::ostream& out, Set& a);
	std::string subset (Element& sbst);
	std::string Sett(Set* some_set);
}
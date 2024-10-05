#pragma once
#pragma once
#include <string>
#include<vector>
#include<iostream>
namespace sets {
	class set;
	class input {
	private:
		std::string line = "";
	public:
		bool sets(set& num_1);
		std::string string_input()&;
		std::string char_input()&;
		std::string getter();
	};
	class element {
	private:
		std::string Element = "";
		set* Subset = nullptr;
	public:
		bool operator ==(const element& anthr_element)const;
		static bool compare_string(const element& a, const element& b);
		element fill(const std::string& Element);
		void del_subset();
		std::string elmnt();
		set* Sub();
	};
	class set {
	private:
		std::vector<element> Set;
		void add_element(const std::string& Element);
		void sort_descending();
		set operation_for_merge( set& num_1,const set& num_2);
		set operation_for_inter(const set& num_1, const set& num_2);
		set operation_for_diff(const set& num_1, const set& num_2);
	public:
		set();
		set(const set& to_copy);
		std::vector<element> getter();
		~set();
		bool check_on_input(const std::string& input);
		bool check_on_repeats();
		void parsing(const std::string& input);
		bool operator ==(const set* anthr_set);
		bool operator !=(const set* anthr_set);
		bool check_on_emptiness();
		void del_element(input elmnt_to_del);
		int  amnt_of_elements();
		set operator +(const set& anthr_set);
		set operator +=(const set& anthr_set);
		set operator *(const set& anthr_set);
		set operator *=(const set& anthr_set);
		int operator [](std::string& elmnt);
		set operator -(const set& anthr_set);
		set operator -=(const set& anthr_set);
		void PowerSet();
	};
	std::string del_all_space(std::string& input);
	std::ostream& operator<<(std::ostream& out, set& a);
	std::string subset(element& subst);
	std::string Set(set* some_set);
}
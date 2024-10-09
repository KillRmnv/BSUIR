#pragma once
#include <string>
#include<vector>
#include<iostream>
namespace sets_ns {
	class Set;
	class Element {
	private:
		std::string element = "";
		Set* Subset = nullptr;
	public:
		bool operator ==(const Element& anthr_element)const;
		static bool compare_string(const Element& a, const Element& b);
		Element fill(const std::string& element);
		void del_subset();
		std::string elmnt();
		Set* Sub();
	};
}
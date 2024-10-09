#pragma once
#include <string>
#include<vector>
#include<iostream>
#include"sets.h"
#include"element.h"
namespace sets_ns {
	class Input_set {
	private:
		std::string line = "";
	public:
		bool Create_set(Set& num_1);
		std::string string_input()&;
		std::string char_input()&;
		std::string getter();
	};
}
#pragma once

#include<string>
#include <iostream>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream> 
class SystemDate{
public:
    std::string get_system_date();
    int get_system_date_int();
};
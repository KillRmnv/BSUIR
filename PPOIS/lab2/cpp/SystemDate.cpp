#include "../src/SystemDate.h"
std::string SystemDate::get_system_date(){
    std::string date;
    auto now = std::chrono::system_clock::now();
    std::time_t current_time = std::chrono::system_clock::to_time_t(now);
    std::tm local_time = *std::localtime(&current_time);
    std::stringstream date_line;
    date= "Date: ";
    date_line<<std::put_time(&local_time, "%Y-%m-%d ");
    date+=date_line.str();
    return date;
}
    int SystemDate::get_system_date_int(){
        std::string date=get_system_date();
            std::string date_part = date.substr(date.find(": ") + 2);
            std::cout<<date_part;
            date_part.erase(date_part.find("-"),1);
            date_part.erase(date_part.find("-"),1);
            std::cout<<date_part;

        int date_in_int=std::stoi(date_part);
        return date_in_int;
    }
#pragma once

#include <string>
#include "Employee.h"
#include <nlohmann/json.hpp>
#include <iostream>
#include"SystemDate.h"
class Comment{
    private:
        std::string text;
        int user_ID;
        std::string date;
    public:
        Comment(std::string Text,int User_ID,std::string Date):
            text{Text},user_ID{User_ID},date{Date}{}
        static Comment from_json(const nlohmann::json & json_comment);
        nlohmann::json to_json() const;
        void DisplayText();
        void Edit(int editing_user_id,std::string Text);
        int get_ID();
        Comment(){}
        std::string get_text();
};

#pragma once

#include <string>
#include <iostream>
#include <nlohmann/json.hpp>
#include "Personal_account.h"

class User {
private:
    int ID = 0;
    std::string position;
     Personal_account Account;
    std::string name;
    std::string secondName;

public:
    User() = default;
    User(int ID, std::string position, std::string name, std::string secondName, Personal_account account);

    int get_ID() const;
     Personal_account& get_account() ;
    std::string get_name();
    nlohmann::json to_json() const;
    static User from_json(const nlohmann::json& json_file);

    void edit(int id,std::string Position,std::string Name,std::string SecondName);
};



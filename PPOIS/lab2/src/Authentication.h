#pragma once
#include <string>
#include<unordered_map>
#include "DocumentWorkflow.h"
class Authentication{
     private:
    int User_ID;
    std::string password;
    std::unordered_map<int,std::string> UserList;
    public:
    void enterInfo(int user_id,std::string Password);
    User try_to_log(DocumentWorkflow& organisation_name);
    Authentication(std::unordered_map<int,std::string> userList):
    UserList(userList){}
    nlohmann::json to_json();
    static Authentication from_json(const nlohmann::json);
    Authentication(){}
    void edit_database(User user,std::string password);
    void del_user(User user);
     bool check_on_emptyness();
     int amnt_of_users();
};
#pragma once

#include <unordered_map>
#include "FileWriter.h"
#include "Personal_account.h"
#include "User.h"

class Department {
private:
    std::unordered_map<int, User> users_by_id; 
    std::unordered_map<int, std::vector<User>> users_by_amount_of_docs; 
public:
    User find_user_by_ID(int ID);       
    Department& del_user(int ID);        
    Department& add_user(User new_user); 
    nlohmann::json to_json_users();
    nlohmann::json to_json_doclists();
    static Department from_json_users(const nlohmann::json json_file);
    static std::unordered_map<int,std::vector<User>> from_json_doclists(const nlohmann::json json_file);
    void distribute_doc(EDocument doc);
    void del_doc(User ID,int amnt);
    int amnt_of_users();
};
   
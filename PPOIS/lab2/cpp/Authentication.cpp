#include "../src/Authentication.h"
#include "../src/Personal_account.h"
void Authentication::enterInfo(int user_id,std::string Password) {
 User_ID=user_id;
password=Password;
}
User Authentication::try_to_log(DocumentWorkflow& organisation_name) {
    if(!UserList.empty()){
    auto it = UserList.find(User_ID);
    if (it != UserList.end()) {
        if (it->second == password) {
            return organisation_name.find_user(User_ID); 
        } else {
            std::cout << "Wrong password!" << std::endl;
        }
    } else {
        std::cout << "User not found!" << std::endl;
    }

    return User();
    }else{
        Personal_account admins;admins.Identify_position("Administrator");
        User admin(1000000001,"Administrator","First","One",admins);
        edit_database(admin,"1234");
        return admin;
    }
}

nlohmann::json Authentication::to_json() {
    nlohmann::json json;
    for (const auto& user : UserList) {
        json[std::to_string(user.first)] = user.second;
    }
    return json;
}

Authentication Authentication::from_json(const nlohmann::json json_file) {
    std::unordered_map<int, std::string> user_list;
    for (auto& item : json_file.items()) {
        int user_id = std::stoi(item.key());
        user_list[user_id] = item.value();
    }
    return Authentication(user_list);
}
   void Authentication::edit_database(User user,std::string password){
    UserList[user.get_ID()]=password;
   }
    void Authentication::del_user(User user){
        UserList.erase(user.get_ID());
    }
    bool Authentication::check_on_emptyness(){
        return UserList.empty();
    }
    int Authentication::amnt_of_users(){
        return UserList.size();
    }
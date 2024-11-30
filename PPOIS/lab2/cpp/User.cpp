#include "../src/User.h"
User::User(int ID, std::string position, std::string name, std::string secondName, Personal_account account)
    : ID(ID), position(std::move(position)), name(std::move(name)), secondName(std::move(secondName)), Account(std::move(account)) {}

int User::get_ID() const {
    return ID;
}

 Personal_account& User::get_account()  {
    return Account;
}

void User::edit(int id,std::string Position,std::string Name,std::string SecondName) {
    ID=id;
    position=Position;
    Account.Identify_position(position);
    name=Name;
    secondName=SecondName;
}

nlohmann::json User::to_json() const {
    return nlohmann::json{
        {"ID", ID},
        {"position", position},
        {"name", name},
        {"secondName", secondName},
        {"Account", Account.to_json()}
    };
}

User User::from_json(const nlohmann::json& json_file) {
    if (!json_file.contains("ID") || !json_file.contains("position") || !json_file.contains("name") || 
        !json_file.contains("secondName") ) {
        throw std::invalid_argument("Invalid JSON structure for User");
    }
     if(json_file.contains("Account"))
    return User{
        json_file["ID"].get<int>(),
        json_file["position"].get<std::string>(),
        json_file["name"].get<std::string>(),
        json_file["secondName"].get<std::string>(),
       
        Personal_account::from_json(json_file["Account"])
    };
    else
        {
            Personal_account acc(json_file["position"].get<std::string>());
     return User{json_file["ID"].get<int>(),
        json_file["position"].get<std::string>(),
        json_file["name"].get<std::string>(),
        json_file["secondName"].get<std::string>(),
        acc
        };
        }
}
    std::string User::get_name(){
        return name;
    }

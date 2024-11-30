#include "../src/Department.h"
  void Department::del_doc(User user,int amnt){
        std::vector<User> Users,    users_minus_one_doc=users_by_amount_of_docs[amnt-1];
        Users=users_by_amount_of_docs[amnt];
        for(int i=0;i<Users.size();i++){
            if(Users[i].get_ID()==user.get_ID()){
                users_minus_one_doc.push_back(user);
                
                Users.erase(Users.begin()+i);
                break;
            }
        }
     }


   User Department::find_user_by_ID(int ID) {
        auto it = users_by_id.find(ID);
        if (it != users_by_id.end()) {
            return it->second; 
        }
        return User(); 
    }


    Department& Department::del_user(int ID) {
        if(find_user_by_ID(ID).get_ID()!=0){
     int amnt_of_docs=find_user_by_ID(ID).get_account().amnt_of_docs();DocsList users_del_list;
        users_by_id.erase(ID); 
        std::vector<User> Users=users_by_amount_of_docs[amnt_of_docs];
        FileWriter docsList;


        for(int i=0;i<Users.size();i++){

            if(ID==Users[i].get_ID()){

                users_del_list=Users[i].get_account().get_list();
                Users.erase(Users.begin()+i);
                users_by_amount_of_docs[amnt_of_docs]=Users;
                docsList.rewrite(to_json_doclists(),"DocsLists");

                for(int i=1;i<amnt_of_docs+1;i++){
                    distribute_doc(users_del_list.pop(i));
                }

                break;
            }
        }
        }
        return *this;
    }


    Department& Department::add_user(User new_user) {

        std::vector<User> new_users;
        users_by_id[new_user.get_ID()] = new_user;
        new_users=users_by_amount_of_docs[0];
        new_users.push_back(new_user);
        users_by_amount_of_docs[0]=new_users;


        FileWriter docsList_file;
        docsList_file.rewrite(to_json_doclists(),"DocsLists");
        return *this;
    }


     nlohmann::json Department::to_json_users() {
        nlohmann::json json_users;

        for (const auto& pair : users_by_id) {
            json_users[std::to_string(pair.first)] = pair.second.to_json(); 
        }

        return json_users;
    }

    Department Department::from_json_users(nlohmann::json json_file) {
        Department department;

        for (auto& item : json_file.items()) {
            department.add_user(User::from_json(item.value()));  
        }

        return department;
    }


void Department::distribute_doc(EDocument doc) {
    if (users_by_amount_of_docs.empty()) {
        return; // Если список пользователей пуст, выходим
    }

    for (int i = 0; ; ++i) {
        auto it = users_by_amount_of_docs.find(i);
        
        if (it == users_by_amount_of_docs.end()) {
            continue; // Если нет пользователей с i документами, продолжаем
        } else {
            User user_to_move = it->second.front(); // Берем первого пользователя
            it->second.erase(it->second.begin()); // Удаляем его из текущего списка

            // Обновляем список дел пользователя
            user_to_move.get_account().updateToDoList(doc);

            // Создаем уведомление
            std::string line = "New document received: " + doc.get_name() + 
                               " ID: " + std::to_string(doc.get_ID()) + 
                               " Date expiry: " + doc.get_date();
            Notification new_note;
            new_note.create_Notification(line);
            user_to_move.get_account().add_notifaction(new_note);

            // Обновляем количество документов
            int new_amnt_of_docs = i + 1;

            // Добавляем пользователя с новым количеством документов
            users_by_amount_of_docs[new_amnt_of_docs].push_back(user_to_move);
            users_by_id[user_to_move.get_ID()] = user_to_move; // Обновляем пользователя по ID

            // Проверяем, нужно ли удалить старый ключ
            if (it->second.empty()) {
                users_by_amount_of_docs.erase(it); // Удаляем ключ, если вектор пуст
            }

            // Записываем изменения в файл
            FileWriter update_json;
            update_json.rewrite(to_json_doclists(), "DocsLists");

            break; // Выходим из цикла после успешного распределения
        }
    }
}
    nlohmann::json Department::to_json_doclists(){
            nlohmann::json json_doclists;
            nlohmann::json Users=nlohmann::json::array();
             for (const auto& pair : users_by_amount_of_docs) {
            for(int i=0;i<pair.second.size();i++)
            Users.push_back(pair.second[i].to_json());
            json_doclists[std::to_string(pair.first)] = Users; 
            Users.clear();
        }
        return json_doclists;
    }


     std::unordered_map<int,std::vector<User>> Department::from_json_doclists(const nlohmann::json json_file){
            std::unordered_map<int, std::vector<User>> doclists;
            for (auto& item : json_file.items()) {
            int amnt_of_docs=std::stoi(item.key());
            std::vector<User> users_from_json;
            for(auto user:item.value()){
                users_from_json.push_back(User::from_json(user));
            }
            doclists[amnt_of_docs]=users_from_json;
        }
        return doclists;
    }
    int Department::amnt_of_users(){

        return users_by_id.size();

    }
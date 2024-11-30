#include "../src/Document.h"
   void Document::Display(int num){
    history.Display(num);
   }

    std::string Document::get_author(){
        return author;
    }
    std::string Document::get_date(){
        return expiry_date;
    }
    std::string Document::get_type(){
        return type;
    }
    std::string Document::get_name(){
        return name;
    }

int Document::get_ID(){
    return ID;
}
 nlohmann::json Document::to_json() const {
    nlohmann::json json_data;

        return nlohmann::json{
            {"type", type},
            {"name", name},
            {"ID", ID},
            {"creation_date", creation_date},
            {"author", author},
            {"expiry_date", expiry_date},
            {"signature", signature},
            {"stamp",stamp},
            {"history",  history.to_json()}
        };
    }
    Document Document::from_json( nlohmann::json json_file) {
            RevisionHistory History;
            if(json_file.contains("history"))
            History.from_json(json_file.at("history").get<nlohmann::json>());
        Document doc(
            json_file.at("type").get<std::string>(), 
            json_file.at("name").get<std::string>(),
            json_file.at("ID").get<int>(),
            json_file.at("creation_date").get<std::string>(),
            json_file.at("author").get<std::string>(),
            json_file.at("expiry_date").get<std::string>(),
            json_file.at("signature").get<bool>(),
            json_file.at("stamp").get<bool>(),
            History
        );
        return doc;
    }
        void Document::info_about_document() {
        std::cout << "Type: " << type << "\n";
        std::cout << "Name: " << name << "\n";
        std::cout << "ID: " << ID << "\n";
        std::cout << "Created on: " << creation_date << "\n";
        std::cout << "Author: " << author << "\n";
        std::cout << "Expiry date: " << expiry_date << "\n";
        std::cout << "Signature: " << (signature ? "Yes" : "No") << "\n";
        std::cout << "Stamp: " << (stamp ? "Yes" : "No") << "\n";
    }
    int Document::get_date_int(){
        expiry_date.erase( expiry_date.begin()+4);
         expiry_date.erase( expiry_date.begin()+6);
        return stoi( expiry_date);

    }
    bool Document::operator==( Document& other)  {
    return get_ID() == other.get_ID();
    }
       std::string Document::get_creation_date(){
        return creation_date;
       }
       std::string Document::get_expiry_date(){
        return expiry_date;
       }
       bool Document::is_stamped(){
        return stamp;
       }
       bool Document::is_signed(){
        return signature;
       }
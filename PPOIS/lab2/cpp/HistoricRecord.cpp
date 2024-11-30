#include "../src/HistoricRecord.h"
    nlohmann::json HistoricRecord::to_json() const {
        return nlohmann::json{
            {"date_arrival", DateArrival},
            {"date_send", DateSend},
            {"note", note.to_json()}
        };
    }
    HistoricRecord HistoricRecord::from_json(const nlohmann::json& json_file) {

        return HistoricRecord(
            json_file.at("date_arrival").get<std::string>(),
            json_file.at("date_send").get<std::string>(),
            Comment::from_json(json_file.at("note"))   
            );
    }
    std::string HistoricRecord::get_date_arrival(){
        return DateArrival;
    }
    std::string HistoricRecord::get_date_send(){
        return DateSend;
    }
    Comment HistoricRecord::get_comment(){
        return note;
    }
    void HistoricRecord::Display(){
        std::cout<<DateArrival<<std::endl<<DateSend<<std::endl;
        note.DisplayText();
    }
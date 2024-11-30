#pragma once

#include<string>
#include "Comment.h"
#include <nlohmann/json.hpp>
class HistoricRecord{
    private:
    std::string DateArrival;
    std::string DateSend;
    Comment note;
    public:
    HistoricRecord(std::string dateArrival, std::string dateSend, Comment chang)
        : DateArrival(dateArrival), DateSend(dateSend), note(chang) {}
    nlohmann::json to_json() const; 
    static HistoricRecord from_json(const nlohmann::json& json_file);
    std::string get_date_arrival();
    std::string get_date_send();
    Comment get_comment();
    void Display();
    HistoricRecord()=default;
};

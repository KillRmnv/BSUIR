#pragma once

#include<string>
#include <nlohmann/json.hpp>
#include"HistoricRecord.h"
#include<iostream>
class RevisionHistory{
    private:
    std::vector<HistoricRecord> history;
    public:
    RevisionHistory& add_new_log(   std::string DateArrival, std::string DateSend,Comment note);
    RevisionHistory&  del_logs(int amnt);
    void  del_exact_log(  std::string DateArrival,std::string DateSend,int num);
    void from_json(nlohmann::json json_file);
    nlohmann::json to_json() const;
    void Display(int num);
    Comment get_comment(int num);
     std::vector<HistoricRecord> get_history() const;
};
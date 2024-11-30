#pragma once
#include <string>
#include <vector>
#include <nlohmann/json.hpp>
#include "Log.h"

class ActivityLog {
private:
    std::vector<Log> user_history;
public:
    void add_new_log(std::string new_action);
    void DisplayLog(int amnt_of_records);
    ActivityLog del(int amnt);

    nlohmann::json to_json() const;
    static ActivityLog from_json(const nlohmann::json& json_file);
};
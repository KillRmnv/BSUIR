#include"../src/ActivityLog.h"
void ActivityLog::add_new_log(std::string new_action) {
    user_history.push_back(Log(new_action));
}

void ActivityLog::DisplayLog(int amnt_of_records) {
    for (size_t i = 0; i < amnt_of_records && i < user_history.size(); i++) {
        user_history[user_history.size() - 1 - i].Display();
    }
}

ActivityLog ActivityLog::del(int amnt) {
    if (amnt < user_history.size()) {
        amnt = user_history.size();
    }
    user_history.erase(user_history.begin() + amnt - 1);
    return *this;
}

nlohmann::json ActivityLog::to_json() const {
    nlohmann::json log_array = nlohmann::json::array();
    for (const auto& log : user_history) {
        log_array.push_back(log.to_json());
    }
    return {
        {"user_history", log_array}
    };
}

ActivityLog ActivityLog::from_json(const nlohmann::json& json_file) {
    ActivityLog activity_log;
    auto logs = json_file.at("user_history").get<std::vector<nlohmann::json>>();
    for (const auto& log_json : logs) {
        activity_log.user_history.push_back(Log::from_json(log_json));
    }
    return activity_log;
}
#include "../src/Log.h"
Log::Log(std::string Action) {
    SystemDate sysdate;
    action = Action;
    date = sysdate.get_system_date();
}

void Log::Display() {
    std::cout << action << " " << date << std::endl;
}

nlohmann::json Log::to_json() const {
    return {
        {"action", action},
        {"date", date}
    };
}

Log Log::from_json(const nlohmann::json& json_file) {
    return Log(
        json_file.at("action").get<std::string>()  
    );
}
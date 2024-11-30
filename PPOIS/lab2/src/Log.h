#pragma once

#include <string>
#include <vector>
#include <nlohmann/json.hpp>
#include "SystemDate.h"

class Log {
private:
    std::string action;
    std::string date;

public:
    Log(std::string Action);
    void Display();
    std::string action_interpret();

    nlohmann::json to_json() const;
    static Log from_json(const nlohmann::json& json_file);
};

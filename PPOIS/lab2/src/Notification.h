#pragma once

#include <string>
#include <iostream>
#include "SystemDate.h"
#include <nlohmann/json.hpp>
class Notification {
private:
    std::string text;
    std::string date;

public:
    void DisplayNotification();
    void create_Notification(std::string new_text);
    static Notification from_json(const nlohmann::json& json_notes);
    nlohmann::json to_json() const;
    
};

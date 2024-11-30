#include "../src/Notification.h"

void Notification::DisplayNotification() {
    std::cout  << text << std::endl;
    std::cout  << date << std::endl;
}

void Notification::create_Notification(std::string new_text) {
    SystemDate sysdate;
    text = new_text;
    date = sysdate.get_system_date(); 
}
nlohmann::json Notification::to_json() const {
    nlohmann::json json_notes;
    json_notes["text"] = text;
    json_notes["date"] = date;
    return json_notes;
}

Notification Notification::from_json(const nlohmann::json& json_notes) {
    Notification notification;
    if (json_notes.contains("text") && json_notes["text"].is_string()) {
        notification.text = json_notes["text"];
    } 

    if (json_notes.contains("date") && json_notes["date"].is_string()) {
        notification.date = json_notes["date"];
    } 

    return notification;
}
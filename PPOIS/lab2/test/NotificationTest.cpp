#include <gtest/gtest.h>
#include "../src/Notification.h"
#include "../src/SystemDate.h"  // Убедитесь, что этот файл существует

class NotificationTest : public ::testing::Test {
protected:
    Notification notification;

    void SetUp() override {
        // Инициализация объекта Notification
        notification.create_Notification("Initial notification text");
    }
};

TEST_F(NotificationTest, CreateNotification) {
    notification.create_Notification("New notification text");
    
    EXPECT_EQ(notification.to_json()["text"], "New notification text");
    // Проверка, что дата была обновлена (формат даты нужно уточнить)
}

TEST_F(NotificationTest, DisplayNotification) {
    testing::internal::CaptureStdout();
    notification.DisplayNotification();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Initial notification text") != std::string::npos);
    // Проверка, что дата отображается (можно уточнить формат)
}

TEST_F(NotificationTest, ToJson) {
    nlohmann::json json_output = notification.to_json();
    
    EXPECT_TRUE(json_output.contains("text"));
    EXPECT_EQ(json_output["text"], "Initial notification text");
    EXPECT_TRUE(json_output.contains("date"));
}

TEST_F(NotificationTest, FromJson) {
    // Тестовые данные JSON
    nlohmann::json json_data = {
        {"text", "Test notification"},
        {"date", "2023-11-21"}  // Убедитесь, что здесь правильная дата
    };

    Notification new_notification = Notification::from_json(json_data);
    
    EXPECT_EQ(new_notification.to_json()["text"], "Test notification");
    EXPECT_EQ(new_notification.to_json()["date"], "2023-11-21"); // Проверка даты, если нужно
}


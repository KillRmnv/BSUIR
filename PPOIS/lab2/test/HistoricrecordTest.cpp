#include <gtest/gtest.h>
#include "../src/HistoricRecord.h"
#include "../src/Comment.h"  // Убедитесь, что этот файл существует

class HistoricRecordTest : public ::testing::Test {
protected:
    HistoricRecord record;
    Comment comment;

    void SetUp() override {
        // Инициализация тестовых данных
        comment = Comment("This is a note.", 1, SystemDate().get_system_date());
        record = HistoricRecord("2023-11-21", "2023-11-22", comment);
    }
};

TEST_F(HistoricRecordTest, ToJson) {
    nlohmann::json json_output = record.to_json();
    
    EXPECT_TRUE(json_output.contains("date_arrival"));
    EXPECT_EQ(json_output["date_arrival"], "2023-11-21");
    EXPECT_TRUE(json_output.contains("date_send"));
    EXPECT_EQ(json_output["date_send"], "2023-11-22");
    EXPECT_TRUE(json_output.contains("note"));
}

TEST_F(HistoricRecordTest, FromJson) {
    // Тестовые данные JSON
    nlohmann::json json_data = {
        {"date_arrival", "2023-11-21"},
        {"date_send", "2023-11-22"},
        {"note", comment.to_json()}
    };

    HistoricRecord new_record = HistoricRecord::from_json(json_data);
    
    EXPECT_EQ(new_record.get_date_arrival(), "2023-11-21");
    EXPECT_EQ(new_record.get_date_send(), "2023-11-22");
    EXPECT_EQ(new_record.get_comment().get_text(), comment.get_text());
}

TEST_F(HistoricRecordTest, GetDateArrival) {
    EXPECT_EQ(record.get_date_arrival(), "2023-11-21");
}

TEST_F(HistoricRecordTest, GetDateSend) {
    EXPECT_EQ(record.get_date_send(), "2023-11-22");
}

TEST_F(HistoricRecordTest, GetComment) {
    EXPECT_EQ(record.get_comment().get_text(), comment.get_text());
}

TEST_F(HistoricRecordTest, Display) {
    testing::internal::CaptureStdout();
    record.Display();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("2023-11-21") != std::string::npos);
    EXPECT_TRUE(output.find("2023-11-22") != std::string::npos);
    EXPECT_TRUE(output.find(comment.get_text()) != std::string::npos);
}

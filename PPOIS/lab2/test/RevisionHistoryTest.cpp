#include <gtest/gtest.h>
#include "../src/RevisionHistory.h"
#include "../src/HistoricRecord.h"
#include "../src/Comment.h"

class RevisionHistoryTest : public ::testing::Test {
protected:
    RevisionHistory revisionHistory;

    void SetUp() override {
        // Инициализация тестовых данных
        Comment comment("Initial log", 1, "2023-11-21");
        revisionHistory.add_new_log("2023-11-21", "2023-11-22", comment);
    }
};

TEST_F(RevisionHistoryTest, AddNewLog) {
    Comment new_comment("Second log", 2, "2023-11-22");
    revisionHistory.add_new_log("2023-11-22", "2023-11-23", new_comment);

    EXPECT_EQ(revisionHistory.get_history().size(), 2);
    EXPECT_EQ(revisionHistory.get_comment(2).get_text(), "Second log");
}

TEST_F(RevisionHistoryTest, Display) {
    testing::internal::CaptureStdout();
    revisionHistory.Display(1);  // Ввод будет нужен для теста
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Initial log") != std::string::npos);
}

TEST_F(RevisionHistoryTest, DelExactLog) {
    revisionHistory.del_exact_log("2023-11-21", "2023-11-22",1);  // Подразумевается, что пользователь введет 1
    std::istringstream input("1");
    std::cin.rdbuf(input.rdbuf());
    EXPECT_EQ(revisionHistory.get_history().size(), 0);
}


TEST_F(RevisionHistoryTest, FromJson) {
    nlohmann::json json_data = {
        {"history", nlohmann::json::array({
            {{"date_arrival", "2023-11-21"}, {"date_send", "2023-11-22"}, {"note", {{"text", "Initial log"}, {"user_ID", 1}, {"date", "2023-11-21"}}}}}
        )}
    };

    revisionHistory.from_json(json_data);

    EXPECT_EQ(revisionHistory.get_history().size(), 2);
    EXPECT_EQ(revisionHistory.get_history()[0].get_date_arrival(), "2023-11-21");
}

TEST_F(RevisionHistoryTest, DelLogs) {
    revisionHistory.del_logs(1);
    EXPECT_EQ(revisionHistory.get_history().size(), 0);
}


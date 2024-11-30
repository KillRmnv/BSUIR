#include <gtest/gtest.h>
#include "../src/FileReader.h"
#include "../src/FileWriter.h"
#include"../src/User.h"
#include <fstream>

class FileReaderTest : public ::testing::Test {
protected:
    FileReader fileReader;
    const std::string test_file_path = "test_file.json";

    void SetUp() override {
        std::remove(test_file_path.c_str());
    }

    void TearDown() override {
        std::remove(test_file_path.c_str());
    }
};

TEST_F(FileReaderTest, CreateNewFile) {
    nlohmann::json json_output = fileReader.build("test_file");
    
    // Проверяем, что файл был создан
    std::ifstream file(test_file_path);
    EXPECT_TRUE(file.is_open());
    file.close();
}

// TEST_F(FileReaderTest, ReadExistingFile) {
//         Personal_account account("Administrator");
//         User user(1, "Administrator", "Lom", "Jones", account);

//       fileReader.build("test_file");
//     FileWriter fileWriter;fileWriter.rewrite(user.to_json(), "test_file");
//    nlohmann::json json_output = fileReader.build("test_file");

//     // Проверяем, что содержимое файла прочитано правильно
//     EXPECT_EQ(json_output.size(), 1);
//     EXPECT_EQ(json_output[0]["name"], "Lom");
//     EXPECT_EQ(json_output[0]["id"], 1);
// }

TEST_F(FileReaderTest, EmptyFile) {
          fileReader.build("test_file");

    nlohmann::json json_output = fileReader.build("test_file");
    
    EXPECT_EQ(json_output.size(), 0);
}

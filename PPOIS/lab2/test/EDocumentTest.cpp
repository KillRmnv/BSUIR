#include <gtest/gtest.h>
#include "../src/EDocument.h"
#include "../src/Comment.h"  // Убедитесь, что этот файл существует
#include "../src/SystemDate.h"  // Убедитесь, что этот файл существует

class EDocumentTest : public ::testing::Test {
protected:
    EDocument doc;

    void SetUp() override {
        doc = EDocument("111111111111111", "Test Document", 1, "2023-11-21", "Alice", "2024-11-21", true, false, RevisionHistory());
        doc.set_path_to_file("C:/path/to/document.txt");
    }
};

TEST_F(EDocumentTest, EditDocument) {
    int user_ID = 1;  
    std::string new_name = "Marelyn Manson";
    std::string new_type = "234556";
    std::string new_creation_date = "2024.10.03";
    std::string new_author = "Rick Ramirez";
    std::string new_expiry_date = "3224.12.31";


    doc.edit(user_ID,"Marelyn Manson","234556","2024.10.03","Rick Ramirez","3224.12.31");

    EXPECT_EQ(doc.get_name(), new_name);
    EXPECT_EQ(doc.get_type(), new_type);
    EXPECT_EQ(doc.get_creation_date(), new_creation_date);
    EXPECT_EQ(doc.get_author(), new_author);
    EXPECT_EQ(doc.get_expiry_date(), new_expiry_date);
}

TEST_F(EDocumentTest, AddComment) {
    Comment comment("This is a comment.", 1, SystemDate().get_system_date());
    doc.add_comment(comment);

    ASSERT_EQ(doc.get_comments().size(), 1);
    EXPECT_EQ(doc.get_comments()[0].get_text(), comment.get_text());
}

TEST_F(EDocumentTest, DisplayComments) {
    Comment comment1("First Comment", 1, SystemDate().get_system_date());
    Comment comment2("Second Comment", 1, SystemDate().get_system_date());
    doc.add_comment(comment1);
    doc.add_comment(comment2);

    // Подмена ввода для теста
    std::istringstream input_stream("2\n");
    std::cin.rdbuf(input_stream.rdbuf());

    // Проверяем, что вывод отображает комментарии
    testing::internal::CaptureStdout();
    doc.DisplayComms(2);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("First Comment") != std::string::npos);
    EXPECT_TRUE(output.find("Second Comment") != std::string::npos);
}

TEST_F(EDocumentTest, ToJson) {
    nlohmann::json json_output = doc.to_json();
    
    EXPECT_TRUE(json_output.contains("path_to_file"));
    EXPECT_EQ(json_output["path_to_file"], "C:/path/to/document.txt");
    EXPECT_TRUE(json_output.contains("Comments_to_doc"));
    EXPECT_EQ(json_output["Comments_to_doc"].size(), 0); // Пока нет комментариев
}

TEST_F(EDocumentTest, FromJson) {
    // Тестовые данные JSON
    nlohmann::json json_data = {
        {"type", "111111111111111"},
        {"name", "Test Document"},
        {"ID", 1},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2024-11-21"},
        {"path_to_file", "C:/path/to/document.txt"},
        {"Comments_to_doc", nlohmann::json::array()},
        {"signature",false},{"stamp",true}
    };

    EDocument new_doc = EDocument::from_json(json_data);
    EXPECT_EQ(new_doc.get_name(), "Test Document");
    EXPECT_EQ(new_doc.get_path_to_file(), "C:/path/to/document.txt");
}
TEST_F(EDocumentTest, ChangeToCopyVersion) {
    std::string original_type = doc.get_type();
    doc.change_to_copy_version();
    
    EXPECT_EQ(doc.get_type(), "111111111111211");
}

TEST_F(EDocumentTest, Approve) {
    doc.aprove();
    EXPECT_TRUE(doc.is_stamped());
}

TEST_F(EDocumentTest, Sign) {
    doc.sign();
    EXPECT_TRUE(doc.is_signed());
}


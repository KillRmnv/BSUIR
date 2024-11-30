#include <gtest/gtest.h>
#include "../src/Document.h"

class DocumentTest : public ::testing::Test {
protected:
    Document doc;

    void SetUp() override {
        // Инициализация документа с тестовыми данными
        doc = Document("Report", "Test Document", 1, "2023-11-21", "Alice", "2024-11-21", true, false, RevisionHistory());
    }
};

TEST_F(DocumentTest, GetAuthor) {
    EXPECT_EQ(doc.get_author(), "Alice");
}

TEST_F(DocumentTest, GetDate) {
    EXPECT_EQ(doc.get_date(), "2024-11-21");
}

TEST_F(DocumentTest, GetType) {
    EXPECT_EQ(doc.get_type(), "Report");
}

TEST_F(DocumentTest, GetName) {
    EXPECT_EQ(doc.get_name(), "Test Document");
}

TEST_F(DocumentTest, GetID) {
    EXPECT_EQ(doc.get_ID(), 1);
}

TEST_F(DocumentTest, ToJson) {
    nlohmann::json expected_json = {
        {"type", "Report"},
        {"name", "Test Document"},
        {"ID", 1},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2024-11-21"},
        {"signature", true},
        {"stamp", false},
        {"history", {}}
    };
    EXPECT_EQ(doc.to_json(), expected_json);
}

TEST_F(DocumentTest, FromJson) {
    nlohmann::json json_file = {
        {"type", "Report"},
        {"name", "Test Document"},
        {"ID", 1},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2024-11-21"},
        {"signature", true},
        {"stamp", false}
    };

    Document new_doc = Document::from_json(json_file);
    EXPECT_EQ(new_doc.get_author(), "Alice");
    EXPECT_EQ(new_doc.get_date(), "2024-11-21");
    EXPECT_EQ(new_doc.get_type(), "Report");
    EXPECT_EQ(new_doc.get_name(), "Test Document");
    EXPECT_EQ(new_doc.get_ID(), 1);
}

TEST_F(DocumentTest, InfoAboutDocument) {
    testing::internal::CaptureStdout(); // Перехват стандартного вывода
    doc.info_about_document();
    std::string output = testing::internal::GetCapturedStdout();
    
    EXPECT_TRUE(output.find("Type: Report") != std::string::npos);
    EXPECT_TRUE(output.find("Name: Test Document") != std::string::npos);
    EXPECT_TRUE(output.find("ID: 1") != std::string::npos);
    EXPECT_TRUE(output.find("Created on: 2023-11-21") != std::string::npos);
    EXPECT_TRUE(output.find("Author: Alice") != std::string::npos);
    EXPECT_TRUE(output.find("Expiry date: 2024-11-21") != std::string::npos);
    EXPECT_TRUE(output.find("Signature: Yes") != std::string::npos);
    EXPECT_TRUE(output.find("Stamp: No") != std::string::npos);
}

TEST_F(DocumentTest, GetDateInt) {
    EXPECT_EQ(doc.get_date_int(), 20241121); // Пример ожидаемого значения
}

TEST_F(DocumentTest, EqualityOperator) {
    Document another_doc = Document("Report", "Another Document", 1, "2023-11-21", "Bob", "2024-11-21", true, false, RevisionHistory());
    EXPECT_TRUE(doc == another_doc);
}


#include <gtest/gtest.h>
#include "../src/DocsList.h"
#include "../src/EDocument.h"  // Убедитесь, что этот файл существует

class DocsListTest : public ::testing::Test {
protected:
    DocsList docsList;

    void SetUp() override {
     Comment note("bruh",1,"2024-12-01");
    RevisionHistory history1;history1.add_new_log("2024-12-01", "2024-12-01",  note);
    EDocument doc1("5676564","Test Document",101,"2024-12-01","me","2030-12-01",false,false,history1,"/home");
         Comment note1("bruh",2,"2024-12-01");
 
        RevisionHistory history2;history2.add_new_log("2023-11-22", "2023-11-22",  note1);

        EDocument doc2("Invoice", "Test Document 2", 2, "2023-11-22", "Bob", "2025-11-22", false, false,history2,"/home/bin");
        docsList.add_doc(doc1);
        docsList.add_doc(doc2);
    }
};

TEST_F(DocsListTest, AddDoc) {
    EXPECT_EQ(docsList.amnt_of_elements(), 2);
    Comment note1("bruh",2,"2024-12-01");
    RevisionHistory history2;history2.add_new_log("2023-11-22", "2023-11-22",  note1);
    EDocument new_doc("Memo", "Test Document 3", 3, "2023-11-23", "Charlie", "2025-11-23", false, false,history2,"home/kirillromanoff");
    docsList.add_doc(new_doc);

    EXPECT_EQ(docsList.amnt_of_elements(), 3);
}

TEST_F(DocsListTest, DisplayList) {
    testing::internal::CaptureStdout();
    
    docsList.DisplayList();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(output.find("Test Document") != std::string::npos);
    EXPECT_TRUE(output.find("Test Document 2") != std::string::npos);
}

TEST_F(DocsListTest, PopDoc) {
    EDocument popped_doc = docsList.pop(1);
    
    EXPECT_EQ(popped_doc.get_name(), "Test Document");
    EXPECT_EQ(docsList.amnt_of_elements(), 2);  // После извлечения остается 2 документа
}

TEST_F(DocsListTest, MarkUsComplete) {
    Document completed_doc = docsList.mark_us_complete(1);
    
    EXPECT_EQ(completed_doc.get_name(), "Test Document");
    EXPECT_EQ(docsList.amnt_of_elements(), 1);  // После завершения остается 1 документ
}

TEST_F(DocsListTest, ToJson) {
    nlohmann::json json_output = docsList.to_json();

    EXPECT_EQ(json_output.size(), 2);
    EXPECT_TRUE(json_output[0].contains("name"));
    EXPECT_EQ(json_output[0]["name"], "Test Document");
}

TEST_F(DocsListTest, FromJson) {
    nlohmann::json json_data = nlohmann::json::array({
        {
            {"type", "Report"},
            {"name", "New Document"},
            {"ID", 3},
            {"creation_date", "2023-11-24"},
            {"author", "David"},
            {"expiry_date", "2025-11-24"},
            {"signature", false},
            {"stamp", false},
            {"path_to_file","/home/bin"}
        },
        {
            {"type", "Invoice"},
            {"name", "Invoice Document"},
            {"ID", 4},
            {"creation_date", "2023-11-25"},
            {"author", "Eve"},
            {"expiry_date", "2025-11-25"},
            {"signature", false},
            {"stamp", true},
            {"path_to_file","/home/bin"}
        }
    });


    DocsList new_docsList = DocsList::from_json(json_data);

    EXPECT_EQ(new_docsList.amnt_of_elements(), 2);  // Проверяем количество документов
    EXPECT_EQ(new_docsList.pop(1).get_name(), "New Document");  // Проверяем первый документ
    EXPECT_EQ(new_docsList.pop(2).get_name(), "Invoice Document");  // Проверяем второй документ
}

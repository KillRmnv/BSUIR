#include <gtest/gtest.h>
#include "../src/Storage.h"
#include "../src/FileWriter.h"  

class StorageTest : public ::testing::Test {
protected:
    Storage storage;

    void SetUp() override {
        // Инициализация с тестовыми данными
        nlohmann::json test_docs = nlohmann::json::array({
            {{"type", "123457"},
        {"name", "Test"},
        {"ID", 21},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2025-11-21"},
        {"path_to_file", "C:/document.txt"},
        {"Comments_to_doc", nlohmann::json::array()},
        {"signature",false},{"stamp",false}},

            {{"type", "11111111"},
        {"name", "Test Document"},
        {"ID", 31},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2026-11-21"},
        {"path_to_file", "some path"},
        {"Comments_to_doc", nlohmann::json::array()},
        {"signature",true},{"stamp",true}}
        });
        storage = Storage(test_docs);
    }
};

TEST_F(StorageTest, AddDocument) {
    nlohmann::json new_doc = {
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

    storage.add_document(new_doc, "test_storage");

    EXPECT_EQ(storage.to_json().size(), 3);
    EXPECT_TRUE(storage.check_for_existance(1));
}

TEST_F(StorageTest, DeleteDocument) {
    nlohmann::json doc_to_delete = {{"type", "11111111"},
        {"name", "Test Document"},
        {"ID", 31},
        {"creation_date", "2023-11-21"},
        {"author", "Alice"},
        {"expiry_date", "2026-11-21"},
        {"path_to_file", "some path"},
        {"Comments_to_doc", nlohmann::json::array()},
        {"signature",true},{"stamp",true}};

    storage.del_doc(Document::from_json(doc_to_delete), "test_storage");

    EXPECT_EQ(storage.to_json().size(), 1);
    EXPECT_FALSE(storage.check_for_existance(1));
}


TEST_F(StorageTest, FindDocumentByID) {
    int input_id = 21;  
    EDocument found_doc = storage.find_doc(input_id);
    
    EXPECT_EQ(found_doc.get_ID(), 21);
}

TEST_F(StorageTest, CheckForExistance) {
    EXPECT_TRUE(storage.check_for_existance(31));
    EXPECT_FALSE(storage.check_for_existance(99));  // Неверный ID
}

TEST_F(StorageTest, DeleteExactDocument) {
    storage.del_exact_doc("test_storage",31);

    EXPECT_EQ(storage.to_json().size(), 1); // После удаления должно остаться 1 документ
}


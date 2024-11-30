#include <gtest/gtest.h>
#include "../src/DocumentWorkflow.h"
#include "../src/Personal_account.h"
#include "../src/User.h"
#include "../src/EDocument.h"
#include "../src/Storage.h"

class DocumentWorkflowTest : public ::testing::Test {
protected:
    DocumentWorkflow workflow;
    User user;
    EDocument doc;

    void SetUp() override {
        Personal_account account("Administrator");
        user = User(1, "Administrator", "Lom", "Jones", account);

        Comment note("Important comment", user.get_ID(), "2024-12-01");
        RevisionHistory history;
        history.add_new_log("2024-12-01", "2024-12-01", note);

        doc = EDocument("Report", "Test Document", 1, "2023-11-21", "Alice", "2024-11-21", true, false, history, "/home/test_file");
        workflow.add_to_storage(doc); // Добавляем документ в хранилище
        user.get_account().updateToDoList(doc);
        workflow.add_user(user);      // Добавляем пользователя

    }
};

// Тест на добавление пользователя
TEST_F(DocumentWorkflowTest, AddUser) {
    Personal_account account("Lawyer");
    User new_user(2, "Lawyer", "Bob", "Smith", account);

    workflow.add_user(new_user);
    EXPECT_NO_THROW(workflow.find_user(new_user.get_ID()));
    EXPECT_EQ(workflow.find_user(new_user.get_ID()).get_name(), "Bob");
}

TEST_F(DocumentWorkflowTest, DeleteUser) {
    workflow.del_user(user);

    EXPECT_EQ(workflow.find_user(user.get_ID()).get_ID(), 0);
}

// Тест на перемещение документа из активного хранилища в архив


// Тест на распределение документа
TEST_F(DocumentWorkflowTest, DistributeDocument) {
    workflow.distribute_doc(1, doc, 1, user);
    // Проверка распределения документа в зависимости от реализации Department
    // Например, проверка, что документ был добавлен в список документов департамента
}

// Тест на преобразование в JSON
TEST_F(DocumentWorkflowTest, ToJson) {
    nlohmann::json json_data = workflow.to_json();

    EXPECT_TRUE(json_data.contains("administration"));
    EXPECT_TRUE(json_data.contains("ActiveDocuments"));
    EXPECT_TRUE(json_data.contains("ArchiveDocuments"));
}



// Тест на удаление документа из активного хранилища
TEST_F(DocumentWorkflowTest, DeleteDocumentFromStorage) {
    workflow.del_from_storage(doc);

    EXPECT_THROW(workflow.get_storage().find_doc(doc.get_ID()), std::exception);
}

// Тест на удаление документа из архива
TEST_F(DocumentWorkflowTest, DeleteDocumentFromArchive) {
    workflow.add_to_archive(doc);
    workflow.del_from_archive(doc);

    EXPECT_THROW(workflow.get_archive().find_doc(doc.get_ID()), std::exception);
}

// Тест на нахождение пользователя
TEST_F(DocumentWorkflowTest, FindUser) {
    User found_user = workflow.find_user(user.get_ID());

    EXPECT_EQ(found_user.get_ID(), user.get_ID());
    EXPECT_EQ(found_user.get_name(), user.get_name());
}


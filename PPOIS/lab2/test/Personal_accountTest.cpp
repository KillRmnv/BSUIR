#include <gtest/gtest.h>
#include "../src/Personal_account.h"
#include "../src/EDocument.h"
#include "../src/Notification.h"
#include "../src/SystemDate.h"

class PersonalAccountTest : public ::testing::Test {
protected:
    Personal_account account;

    void SetUp() override {
        // Инициализация объекта Personal_account с тестовыми данными
        account = Personal_account("Administrator");
    }
};

TEST_F(PersonalAccountTest, CreateDoc) {

    SystemDate date;
    EDocument doc = account.create_doc(1,"78956","R.I.P.",42,"2023-11-21","Alice","2025-11-21",date,"C:/path/to/document.txt");
    
    EXPECT_EQ(doc.get_name(), "R.I.P.");
    EXPECT_EQ(doc.get_creation_date(), "2023-11-21");
    EXPECT_EQ(doc.get_author(), "Alice");
    EXPECT_EQ(doc.get_expiry_date(), "2025-11-21");
    EXPECT_EQ(doc.get_path_to_file(), "C:/path/to/document.txt");
}

TEST_F(PersonalAccountTest, CopyDocument) {
     SystemDate date;
    EDocument original_doc = account.create_doc(1,"78956","R.I.P.",42,"2023-11-21","Alice","2025-11-21",date,"C:/path/to/document.txt");;
    account.set_doc(original_doc);

    EDocument copied_doc = account.copy();

    EXPECT_NE(copied_doc.get_name(), original_doc.get_name()); 
    EXPECT_EQ(copied_doc.get_type(), original_doc.get_type());
}

TEST_F(PersonalAccountTest, AddNotification) {
    Notification notification;
    notification.create_Notification("New notification");

    account.add_notifaction(notification);

    EXPECT_EQ(account.get_notifications().size(), 1);
    EXPECT_EQ(account.get_notifications()[0].to_json()["text"], "New notification");
}

TEST_F(PersonalAccountTest, ToJson) {
    nlohmann::json json_output = account.to_json();

    EXPECT_TRUE(json_output.contains("ToDoDocs"));
    EXPECT_TRUE(json_output.contains("user_history"));
    EXPECT_TRUE(json_output.contains("current_doc"));
    EXPECT_TRUE(json_output.contains("receipts"));
    EXPECT_TRUE(json_output.contains("Employee"));
}

// TEST_F(PersonalAccountTest, FromJson) {
//     // Тестовые данные JSON

 
//         nlohmann::json json =  {
//             {"type", "Report"},
//             {"name", "New Document"},
//             {"ID", 3},
//             {"creation_date", "2023-11-24"},
//             {"author", "David"},
//             {"expiry_date", "2025-11-24"},
//             {"signature", false},
//             {"stamp", false},
//             {"path_to_file","/home/bin"}
//         };
//           DocsList list;list.add_doc(EDocument::from_json(json));
//         json={
//             {"type", "Invoice"},
//             {"name", "Invoice Document"},
//             {"ID", 4},
//             {"creation_date", "2023-11-25"},
//             {"author", "Eve"},
//             {"expiry_date", "2025-11-25"},
//             {"signature", false},
//             {"stamp", true},
//             {"path_to_file","/home/bin"}
//         };
//     list.add_doc(EDocument::from_json(json));
//      Comment comment("Initial log", 1, "2023-11-21");
//      RevisionHistory revisionHistory;
//         revisionHistory.add_new_log("2023-11-21", "2023-11-22", comment);
//            nlohmann::json data = {
//         {"type", "111111111111111"},
//         {"name", "Test Document"},
//         {"ID", 1},
//         {"creation_date", "2023-11-21"},
//         {"author", "Alice"},
//         {"expiry_date", "2024-11-21"},
//         {"path_to_file", "C:/path/to/document.txt"},
//         {"Comments_to_doc", nlohmann::json::array()},
//         {"signature",false},{"stamp",true}
//     };
//     Notification notification;
//         notification.create_Notification("Initial notification text");

//     nlohmann::json json_data = {
//         {"ToDoDocs", list.to_json()},
//         {"user_history", revisionHistory.to_json()},
//         {"current_doc", data},
//         {"receipts", notification.to_json()},
//         {"Employee", {{"position", "Administrator"}, {"Department", 1}}}
//     };

//     Personal_account new_account = Personal_account::from_json(json_data);

//     EXPECT_EQ(new_account.get_position()->get_department(), 1);
// }

// TEST_F(PersonalAccountTest, ChooseFromList) {
//     // Добавляем тестовые документы в список
//         SystemDate date;
//     EDocument doc1 = account.create_doc(1,"78956","R.I.P.",42,"2023-11-21","Alice","2025-11-21",date,"C:/path/to/document.txt");;
//     account.updateToDoList(doc1);

//     EDocument chosen_doc = account.choose_from_list(1);
//     EXPECT_EQ(chosen_doc.get_name(), doc1.get_name());
    
// }


#include "../src/Department.h"
#include "gtest/gtest.h"



TEST(DepartmentTest, AddUser) {
    Department department;
    Personal_account account;account.Identify_position("Lawyer");
    User user(1, "Manager", "John", "Doe", account); // Предположим, что Personal_account доступен.
    
    department.add_user(user);
    EXPECT_EQ(department.find_user_by_ID(1).get_ID(), 1);
}

TEST(DepartmentTest, DelUser) {
    Department department;
    Personal_account account;
    User user(1, "Manager", "John", "Doe", account);
    department.add_user(user);
    
    department.del_user(1);
    EXPECT_EQ(department.find_user_by_ID(1).get_ID(), 0); // User не найден.
}

TEST(DepartmentTest, FindUserByID) {
    Department department;
    Personal_account account;
    User user(2, "Developer", "Jane", "Doe", account);
    department.add_user(user);
    
    User found_user = department.find_user_by_ID(2);
    EXPECT_EQ(found_user.get_ID(), 2);
    EXPECT_EQ(found_user.get_name(), "Jane");
}

TEST(DepartmentTest, DistributeDoc) {
    Department department;
    Personal_account account1, account2;
    User user1(1, "Administrator", "John", "Doe", account1);
    department.add_user(user1);
        EXPECT_EQ(department.amnt_of_users(),1);
    Comment note("bruh",user1.get_ID(),"2024-12-01");
    RevisionHistory history;history.add_new_log("2024-12-01", "2024-12-01",  note);
    EDocument doc("5676564","Test Document",101,"2024-12-01","me","2030-12-01",false,false,history,"/home"); 
    department.distribute_doc(doc);
    
    User updated_user = department.find_user_by_ID(1);
    std::cout<<updated_user.get_ID();
    EXPECT_TRUE(updated_user.get_account().has_document(101));
    EXPECT_EQ(updated_user.get_account().get_list().amnt_of_elements(),1);
}

TEST(DepartmentTest, DelDoc) {
    Department department;
    Personal_account account;
    User user(1, "Developer", "Bob", "Jones", account);
     Comment note("bruh",user.get_ID(),"2024-12-01");
    RevisionHistory history;history.add_new_log("2024-12-01", "2024-12-01",  note);
    EDocument doc("5676564","Test Document",101,"2024-12-01","me","2030-12-01",false,false,history,"/home"); 
        department.add_user(user);
    user.get_account().updateToDoList(doc); // Добавляем документ в учетную запись.
    department.distribute_doc(doc);
    Comment note1("bruh",user.get_ID(),"2024-12-01");
    RevisionHistory history1;history1.add_new_log("2024-12-01", "2024-12-01",  note);
    EDocument doc1("786796","Document",102,"2024-12-01","me","2030-12-01",false,false,history,"/home"); 
    
        user.get_account().updateToDoList(doc1); 
        department.distribute_doc(doc1);


    
    department.del_doc(user, 2); // Удаляем документ.

    EXPECT_EQ(user.get_account().get_list().amnt_of_elements(),department.find_user_by_ID(user.get_ID()).get_account().amnt_of_docs());

}

TEST(DepartmentTest, SerializationUsers) {
    Department department;
    Personal_account account1, account2;
    User user1(1, "Manager", "John", "Doe", account1);
    User user2(2, "Developer", "Alice", "Smith", account2);
    department.add_user(user1);
    department.add_user(user2);

    nlohmann::json json_users = department.to_json_users();
    EXPECT_EQ(json_users["1"]["name"], "John");
    EXPECT_EQ(json_users["2"]["name"], "Alice");
}

TEST(DepartmentTest, DeserializationUsers) {
    nlohmann::json json_users = {
        {"1", {{"ID", 1}, {"position", "Manager"}, {"name", "John"}, {"secondName", "Doe"}}},
        {"2", {{"ID", 2}, {"position", "Developer"}, {"name", "Alice"}, {"secondName", "Smith"}}}
    };

    Department department = Department::from_json_users(json_users);
    EXPECT_EQ(department.find_user_by_ID(1).get_name(), "John");
    EXPECT_EQ(department.find_user_by_ID(2).get_name(), "Alice");
}

TEST(DepartmentTest, SerializationDocLists) {
    Department department;
    Personal_account account1, account2;
    User user1(1, "Manager", "John", "Doe", account1);
    User user2(2, "Developer", "Alice", "Smith", account2);
    department.add_user(user1);
    department.add_user(user2);

    nlohmann::json json_doclists = department.to_json_doclists();
    EXPECT_TRUE(json_doclists.contains("0"));  // Проверка, что существует запись для количества документов 0.
}

TEST(DepartmentTest, DeserializationDocLists) {
    nlohmann::json json_doclists = {
        { "0", nlohmann::json::array({
            { {"ID", 1}, {"position", "Manager"}, {"name", "John"}, {"secondName", "Doe"} }
        })},
        { "1", nlohmann::json::array({
            { {"ID", 2}, {"position", "Developer"}, {"name", "Alice"}, {"secondName", "Smith"} }
        })}
    };

    std::unordered_map<int, std::vector<User>> doclists = Department::from_json_doclists(json_doclists);
    EXPECT_EQ(doclists[0][0].get_name(), "John");
    EXPECT_EQ(doclists[1][0].get_name(), "Alice");
}

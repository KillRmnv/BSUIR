#include "../src/Authentication.h"
#include "gtest/gtest.h"

class AuthenticationTest : public ::testing::Test {
protected:
    void SetUp() override {
        userList = {{1001, "password123"}, {1002, "admin2024"}};
        auth = Authentication(userList);
        organisation = DocumentWorkflow();
        Personal_account account;
        User user(1001,"Administrator","Jack","Daniels",account);
        organisation.add_user(user);
        user.edit(1002, "Lawyer", "Nelson", "Mandella");
        organisation.add_user(user);
    }



    std::unordered_map<int, std::string> userList;
    Authentication auth;
    DocumentWorkflow organisation;
};

TEST_F(AuthenticationTest, SuccessfulLogin) {
   auth.enterInfo(1001, "password123");

    User user = auth.try_to_log(organisation);
    EXPECT_EQ(user.get_ID(), 1001);
}

TEST_F(AuthenticationTest, WrongPassword) {
    auth.enterInfo(1001,"nwrongpassword");
    User user = auth.try_to_log(organisation);
    EXPECT_EQ(user.get_ID(), 0); // Ожидается, что ID будет равен 0 при неудачном входе.
}

TEST_F(AuthenticationTest, NonexistentUser) {
        auth.enterInfo(9999,"passwor123");
    User user = auth.try_to_log(organisation);
    EXPECT_EQ(user.get_ID(), 0);
}

TEST_F(AuthenticationTest, CreateAdminOnEmpty) {
    Authentication emptyAuth; // Пустой объект аутентификации.
    User user = emptyAuth.try_to_log(organisation);

    EXPECT_EQ(user.get_ID(), 1000000001); // Проверка, что ID соответствует администратору.
    EXPECT_EQ(user.get_account().get_position()->to_string(), "Administrator");
}

TEST_F(AuthenticationTest, AddUser) {
    User newUser(2002, "Lawyer", "John", "Doe", Personal_account("Lawyer"));
    auth.edit_database(newUser, "3478");
    EXPECT_FALSE(auth.check_on_emptyness());
    EXPECT_EQ(auth.amnt_of_users(), 3) ; // Проверка, что база данных не пуста.
}

TEST_F(AuthenticationTest, DeleteUser) {
    User newUser(2002, "Lawyer", "John", "Doe", Personal_account("Lawyer"));
    auth.edit_database(newUser, "1488");
    auth.del_user(newUser);

    EXPECT_EQ(auth.amnt_of_users(), 2) ;// Проверка, что пользователь удалён, и база данных пуста.
}

TEST_F(AuthenticationTest, ToJsonAndFromJson) {
    User newUser(2002, "Lawyer", "John", "Doe", Personal_account("Lawyer"));

    auto jsonData = auth.to_json();
    Authentication restoredAuth = Authentication::from_json(jsonData);

    EXPECT_FALSE(restoredAuth.check_on_emptyness()); // Проверка, что восстановленный объект содержит данные.
}


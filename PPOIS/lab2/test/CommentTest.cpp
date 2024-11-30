#include "../src/Comment.h"
#include "gtest/gtest.h"



TEST(CommentTest, ToJsonSerialization) {
    Comment comment("This is a test comment.", 101, "2024-11-20");

    nlohmann::json json = comment.to_json();
    EXPECT_EQ(json["text"], "This is a test comment.");
    EXPECT_EQ(json["user_ID"], 101);
    EXPECT_EQ(json["date"], "2024-11-20");
}

TEST(CommentTest, FromJsonDeserialization) {
    nlohmann::json json_comment = {
        {"text", "Deserialized comment."},
        {"user_ID", 102},
        {"date", "2024-11-20"}
    };

    Comment comment = Comment::from_json(json_comment);
    EXPECT_EQ(comment.to_json()["text"], "Deserialized comment.");
    EXPECT_EQ(comment.to_json()["user_ID"], 102);
    EXPECT_EQ(comment.to_json()["date"], "2024-11-20");
}

TEST(CommentTest, EditMethod) {
    Comment comment("Old comment", 101, "2024-11-20");


    comment.Edit(102,"Vabalabda");
    EXPECT_EQ(comment.to_json()["text"], "Vabalabda");
    EXPECT_EQ(comment.to_json()["user_ID"], 102);
    EXPECT_EQ(comment.to_json()["date"], "Date: 2024-11-30 "); // Фиксированная дата.
}

TEST(CommentTest, GetID) {
    Comment comment("Sample comment", 101, "2024-11-20");
    EXPECT_EQ(comment.get_ID(), 101);
}

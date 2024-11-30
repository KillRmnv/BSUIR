#include "../src/SystemDate.h"
#include <gtest/gtest.h>

TEST(SystemDateTest, GetSystemDate) {
    SystemDate date;
    std::string result = date.get_system_date();
    ASSERT_FALSE(result.empty());
    ASSERT_NE(result.find("Date:"), std::string::npos);
}

TEST(SystemDateTest, GetSystemDateInt) {
    SystemDate date;
    int result = date.get_system_date_int();
    ASSERT_GT(result, 0);
}


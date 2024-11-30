#include <gtest/gtest.h>
#include "../src/Employee.h"

class EmployeeTest : public ::testing::Test {
protected:
    Employee emp;

    void SetUp() override {
        emp = Employee(1,"Developer");
    }
};

TEST_F(EmployeeTest, GetDepartment) {
    EXPECT_EQ(emp.get_department(), 1);
}

TEST_F(EmployeeTest, ToString) {
    EXPECT_EQ(emp.to_string(), "Developer");
}

TEST_F(EmployeeTest, ToJson) {
    nlohmann::json json_output = emp.to_json();
    
    EXPECT_TRUE(json_output.contains("position"));
    EXPECT_EQ(json_output["position"], "Developer");
    EXPECT_TRUE(json_output.contains("Department"));
    EXPECT_EQ(json_output["Department"], 1);
}


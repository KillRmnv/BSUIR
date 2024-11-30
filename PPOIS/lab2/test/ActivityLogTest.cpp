#include "../src/ActivityLog.h"
#include <clocale>
#include<gtest/gtest.h>

class ActivityLogTest:public::testing::Test{
    protected:
    void SetUp() override {
        example.add_new_log("add initial log");
    }
    ActivityLog example;
    
};
TEST_F(ActivityLogTest,AddNewLog){
        std::locale("ru_RU.UTF-8");
    example.add_new_log("second log");
       testing::internal::CaptureStdout();
    example.DisplayLog(2);  
    std::string output = testing::internal::GetCapturedStdout();
        EXPECT_EQ(output,"second log Date: 2024-11-30 \nadd initial log Date: 2024-11-30 \n")<< "Output mismatch:\n" 
                                        << "Expected: " << "second log Date: 2024-11-30 \nadd initial log Date: 2024-11-30 \n" 
                                        << "\nActual: " << output;

}
TEST_F(ActivityLogTest,Display){
    std::locale("ru_RU.UTF-8");
       testing::internal::CaptureStdout();
    example.DisplayLog(1);  
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"add initial log Date: 2024-11-30 \n")<< "Output mismatch:\n" 
                                        << "Expected: " << "add initial log Date: 2024-11-30 \n"
                                        << "\nActual: " << output;

}
TEST_F(ActivityLogTest,Del){
    std::locale("ru_RU.UTF-8");
    example.add_new_log("second log");
    example.del(1);
           testing::internal::CaptureStdout();
    example.DisplayLog(1);  
    std::string output = testing::internal::GetCapturedStdout();
        EXPECT_EQ(output,"add initial log Date: 2024-11-30 \n")<< "Output mismatch:\n" 
                                        << "Expected: " << "add initial log Date: 2024-11-30 \n"
                                        << "\nActual: " << output;
;
}
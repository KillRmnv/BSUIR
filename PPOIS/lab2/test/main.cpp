#include "AuthenticationTest.cpp"
#include "CommentTest.cpp"
#include "DepartmentTest.cpp"
#include "DocListTest.cpp"
#include "DocumentTest.cpp"
#include "DocumentWorkflowTest.cpp"
#include "EDocumentTest.cpp"
#include "EmployeeTest.cpp"
#include "FileReaderTest.cpp"
#include "HistoricrecordTest.cpp"
#include "NotificationTest.cpp"
#include "Personal_accountTest.cpp"
#include "RevisionHistoryTest.cpp"
#include "StorageTest.cpp"
#include "SysDateTest.cpp"
#include "ActivityLogTest.cpp"


int main(int argc, char** argv) {
    setlocale(LC_ALL, "ru");
        std::locale::global(std::locale("ru_RU.UTF-8")); 
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS(); 
}
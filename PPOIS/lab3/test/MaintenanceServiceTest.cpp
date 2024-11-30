#include "../Headers/MaintenanceService.h"
#include "../Headers/Aircraft.h"
#include "../Headers/Employee.h"
#include <gtest/gtest.h>

TEST(MaintenanceServiceTests, AddAircraftToMaintenanceList_NoDuplicates) {
    MaintenanceService service;
    Aircraft* aircraft1 = new Aircraft(101, "Boeing 737", true, 80, 200);
    Aircraft* aircraft2 = new Aircraft(101, "Airbus A320", true, 90, 180); // тот же ID
        service.addAircraftToMaintenanceList(aircraft1);

    testing::internal::CaptureStdout();
    service.addAircraftToMaintenanceList(aircraft2);
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output, "Plane with such ID already in service");

    delete aircraft1;
    delete aircraft2;
}

TEST(MaintenanceServiceTests, AddAircraftToMaintenanceList_Success) {
    MaintenanceService service;
    Aircraft* aircraft1 = new Aircraft(101, "Boeing 737", true, 80, 200);
    Aircraft* aircraft2 = new Aircraft(102, "Airbus A320", true, 90, 180);

    service.addAircraftToMaintenanceList(aircraft1);
    service.addAircraftToMaintenanceList(aircraft2);

    // Проверяем, что самолеты добавлены успешно
    EXPECT_EQ(service.getAircraftInMaintenanceCount(), 2);

    delete aircraft1;
    delete aircraft2;
}

// Тест для метода completeMaintenance
TEST(MaintenanceServiceTests, CompleteMaintenance_Success) {
    MaintenanceService service;
    Aircraft* aircraft1 = new Aircraft(101, "Boeing 737", true, 80, 200);

    service.addAircraftToMaintenanceList(aircraft1);

    Aircraft* completed = service.completeMaintenance();

    EXPECT_EQ(completed->getID(), 101);
    EXPECT_EQ(service.getAircraftInMaintenanceCount(), 0);

    delete aircraft1;
}

TEST(MaintenanceServiceTests, CompleteMaintenance_EmptyList) {
    MaintenanceService service;
    testing::internal::CaptureStdout();
    service.completeMaintenance();
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"List is empty");
}

TEST(MaintenanceServiceTests, AddEmployee_NoDuplicates) {
    MaintenanceService service;
    Employee* employee1 = new Employee("Technician", "Day", 1, "Task1");
    Employee* employee2 = new Employee("Technician", "Night", 1, "Task2"); // тот же ID

    service.AddEmployee(employee1);

  testing::internal::CaptureStdout();
    service.AddEmployee(employee2);
        std::string output = testing::internal::GetCapturedStdout();
            EXPECT_EQ(output,"Such employee already exist");

    delete employee1;
    delete employee2;
}

TEST(MaintenanceServiceTests, AddEmployee_Success) {
    MaintenanceService service;
    Employee* employee1 = new Employee("Technician", "Day", 1, "Task1");
    Employee* employee2 = new Employee("Technician", "Night", 2, "Task2");

    service.AddEmployee(employee1);
    service.AddEmployee(employee2);

    EXPECT_NO_THROW(service.AddEmployee(employee1));
    EXPECT_NO_THROW(service.AddEmployee(employee2));

    delete employee1;
    delete employee2;
}

TEST(MaintenanceServiceTests, FireEmployee_Success) {
    MaintenanceService service;
    Employee* employee1 = new Employee("Technician", "Day", 1, "Task1");
    Employee* employee2 = new Employee("Technician", "Night", 2, "Task2");

    service.AddEmployee(employee1);
    service.AddEmployee(employee2);

    service.FireEmployee(employee1);

    EXPECT_NO_THROW(service.FireEmployee(employee2));

    delete employee1;
    delete employee2;
}

TEST(MaintenanceServiceTests, FireEmployee_NotFound) {
    MaintenanceService service;
    Employee* employee1 = new Employee("Technician", "Day", 1, "Task1");

    service.AddEmployee(employee1);

    Employee* employeeNotAdded = new Employee("Technician", "Night", 2, "Task2");
      testing::internal::CaptureStdout();
    service.FireEmployee(employeeNotAdded);
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"There are no employee with such ID");

    delete employee1;
    delete employeeNotAdded;
}

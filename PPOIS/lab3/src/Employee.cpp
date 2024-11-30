#include"../Headers/Employee.h"
void Employee::assignTaskToEmployee(const std::string& task){
Task=task;
}
bool Employee::isEmployeeAvailable() const{
return isAvailable;
}
std::string Employee::getEmployeePosition() const{
return position;
}
int Employee::getID(){
return employeeID;
}

#pragma once

#include"Person.h"
class Employee :public Person{
private:
std::string position;
std::string schedule;
int employeeID;
bool isAvailable;
std::string Task;
public:
void assignTaskToEmployee(const std::string& task); 
bool isEmployeeAvailable() const;
std::string getEmployeePosition() const; 
Employee()=default;
Employee(std::string Position,std::string Schedule,int ID,std::string task):
position(Position),schedule(Schedule),employeeID(ID),isAvailable(true),Task(task){}
int getID();
};
#pragma once
#include <string>
#include <nlohmann/json.hpp>

class Employee {
protected:
    int Department;
    std::string position;

public:
    virtual ~Employee() = default; 
    virtual std::string to_string();
    virtual int get_department();
    virtual nlohmann::json to_json();
     virtual bool canCopy() { return false; }
    virtual bool canEdit() { return false; }
    virtual bool canArchive() { return false; }
    Employee(int department, std::string pos):
    Department(department), position(pos) {}
    Employee()=default;
};


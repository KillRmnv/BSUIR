#pragma once
#include "Employee.h"



class Administrator : public Employee
                     {
public:
    Administrator();
    

    bool canCopy() override { return true; }
    bool canEdit() override { return true; }
    bool canArchive() override { return true; }
};
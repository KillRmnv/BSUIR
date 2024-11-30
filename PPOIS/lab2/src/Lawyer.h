#pragma once

#include "Employee.h"
class Lawyer: public Employee{
         public:
   Lawyer();
     bool canCopy() override { return false; }
    bool canEdit() override { return true; }
    bool canArchive() override { return false; }
};

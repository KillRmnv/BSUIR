#pragma once
#include "Employee.h"

class Bookkeeper: public Employee{
public:
  Bookkeeper();
     bool canCopy() override { return true; }
    bool canEdit() override { return true; }
    bool canArchive() override { return true; }
};

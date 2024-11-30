#pragma once

#include "Aircraft.h"
#include <vector>
class MaintenanceService{
    private:
std::vector<Aircraft*> aircraftList;
std::vector<Employee*> techitians;
public:
void addAircraftToMaintenanceList(Aircraft* aircraft); 
int getAircraftInMaintenanceCount() const; 
Aircraft* completeMaintenance();
void AddEmployee(Employee* newOne);
void FireEmployee(Employee* toFire);
};
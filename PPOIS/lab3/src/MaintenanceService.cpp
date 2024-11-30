#include"../Headers/MaintenanceService.h"
void MaintenanceService::addAircraftToMaintenanceList(Aircraft* aircraft){
    for(auto const aircraftToCompare:aircraftList){
        if(aircraft->getID()==aircraftToCompare->getID()){
            std::cout<<"Plane with such ID already in service";
            return;
        }
    }
aircraftList.push_back(aircraft);
aircraft->setStatus(false);
}
int MaintenanceService::getAircraftInMaintenanceCount() const {
    return aircraftList.size();
} 
Aircraft* MaintenanceService::completeMaintenance(){
    if(!aircraftList.empty()){
        Aircraft* ToComplete=aircraftList[aircraftList.size()-1];
        aircraftList.erase(aircraftList.begin()+(aircraftList.size()-1));
        return ToComplete;
    }
    std::cout<<"List is empty";
}
void MaintenanceService::AddEmployee(Employee* newOne){
    for(auto const technitian:techitians){
        if(newOne->getID()==technitian->getID()){
            std::cout<<"Such employee already exist";
            return;
        }
    }
    techitians.push_back(newOne);
}
void MaintenanceService::FireEmployee(Employee* toFire){
for(size_t i=0;i<techitians.size();i++){
    if(toFire->getID()==techitians[i]->getID()){
            techitians.erase(techitians.begin()+i);
        }
    }
    std::cout<<"There are no employee with such ID";
}
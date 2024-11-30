#pragma once
#include"ServiceCar.h"
#include"Aircraft.h"
class Runway{
    private:
int runwayNumber;
bool isOccupied;
Aircraft* aircraftOnLine;
ServiceCar* baggageCar;
ServiceCar* fuelCar;
public:
public:
void setNewAircraft(Aircraft*newOne);
Aircraft* getAircraft();
void updateStatus(bool newStatus);
bool getStatus();
void landPlane(Aircraft* newOne,std::string location);
ServiceCar* getFuelCar();
ServiceCar* getBaggageCar();
Runway()=default;
Runway(int Num);
void setBaggageCar(ServiceCar* BaggageCar);
void setFuelCar(ServiceCar* FuelCar);

};
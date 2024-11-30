#include"../Headers/Runway.h"
void Runway::setNewAircraft(Aircraft*newOne){
    aircraftOnLine=newOne;
    isOccupied=true;
}
Aircraft* Runway::getAircraft(){
    if(aircraftOnLine!=nullptr)
return aircraftOnLine;
}
void Runway::updateStatus(bool newStatus){
isOccupied=newStatus;
}
bool Runway::getStatus(){
return isOccupied;
}
void Runway::landPlane(Aircraft* newOne,std::string location){
    setNewAircraft(newOne);
    newOne->getOfPlane(location);
    newOne->setStatus(false);
}
Runway::Runway(int Num){
runwayNumber=Num;
isOccupied=false;
}
void Runway::setBaggageCar(ServiceCar* BaggageCar){
baggageCar=BaggageCar;
}
void Runway::setFuelCar(ServiceCar* FuelCar){
fuelCar=FuelCar;
}
ServiceCar* Runway::getFuelCar(){
return fuelCar;
}
ServiceCar* Runway::getBaggageCar(){
return baggageCar;
}
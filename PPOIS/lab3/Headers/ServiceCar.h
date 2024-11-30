#pragma once

#include "Aircraft.h"
#include<vector>
class ServiceCar:Vehicle{
private:
std::string carType; //тип машины (топливозаправщик, грузовик).
public:
void transportBaggageToAircraft( std::vector<Baggage*> baggage,Aircraft* aircraftToDeliver);
void fuelAircraft(Aircraft* aircraftToFuel);
ServiceCar(std::string type);
ServiceCar()=default;
};
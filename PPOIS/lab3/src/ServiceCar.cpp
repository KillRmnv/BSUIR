#include"../Headers/ServiceCar.h"

void ServiceCar::transportBaggageToAircraft( std::vector<Baggage*> baggage,Aircraft* aircraftToDeliver){

}
void ServiceCar::fuelAircraft(Aircraft* aircraftToFuel){
aircraftToFuel->fillWithFuel();
}
ServiceCar::ServiceCar(std::string type){
if(type!="refueler"||type!="bus"){
    //Throw exception
}else
    carType=type;
}
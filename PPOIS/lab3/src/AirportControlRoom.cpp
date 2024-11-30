#include"../Headers/AirportControlRoom.h"
void AirportControlRoom::recieveAircraft(Aircraft* newOne){
    SysDate date;
    for(auto const flight:newOne->getFlights()){
        if(flight->getDestination()==location&&date.getSysDate()==flight->getDate()){
                for(auto const runway:runways){
                    if(!runway->getStatus()){
                    runway->landPlane(newOne,location);
                    return;
                    }
                }
                return;
        }
    }
}
Aircraft* AirportControlRoom::sendAircraft(){
    SysDate date;
    for(auto const runway:runways){
        for(auto const flight:runway->getAircraft()->getFlights()){
            if(flight->getDate()==date.getSysDate()){
                if(runway->getAircraft()->getFuel()<10){
                    runway->getFuelCar()->fuelAircraft(runway->getAircraft());
                }
                return runway->getAircraft();
            }
        }
    }
}
AirportControlRoom::AirportControlRoom(std::string Location,std::vector<Runway*> Runways){
location=Location;
runways=Runways;
}


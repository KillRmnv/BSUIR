#include"../Headers/Airline.h"
void Airline::addAircraft(Aircraft* aircraft){
fleet.push_back(aircraft);
}
void Airline::removeAircraft(Aircraft* aircraft,std::vector<Flight*>& toDistibute){
    if(!fleet.empty()){
    for(size_t i=0;fleet.size();i++){
        if(aircraft->getID()==fleet[i]->getID()){
            toDistibute=fleet[i]->getFlights();
            fleet.erase(fleet.begin()+i);
            break;
            }
        }
    }else{
        std::cout<<"Hangar is empty";
    }
} 
std::vector<Aircraft*> Airline::getAvailableAircraft(std::string date) const{
std::vector<Aircraft*> availablePlane;bool check=false;
    for(auto const plane:fleet){
        check=false;
            for(auto const flight:plane->getFlights()){
                    if(flight->getDate()==date)
                        check=true;
                    }
        if(!check){
            availablePlane.push_back(plane);
        }
    }
return availablePlane;
}
std::vector<Flight*> Airline::getFlightsForDestination(const std::string& destination){
    std::vector<Flight*> availableFlights;
    for(auto const place:destinations){
        if(place->getDestination()==destination)
        availableFlights.push_back(place);
    }
    return availableFlights;
}
void Airline::scheduleFlight(Flight* flight){
    destinations.push_back(flight);
    std::vector<Aircraft*> availablePlanes=getAvailableAircraft(flight->getDate());
    if(!availablePlanes.empty())
    availablePlanes[0]->assignFlight(flight);
    else
     std::cout<<"There are no available planes";
}
Airline::Airline(std::string Name,std::string Id,std::vector<Aircraft*> Fleet, std::vector<Flight*> Destinations){
name=Name;ID=Id;fleet=Fleet;destinations=Destinations;
}
Aircraft* Airline::findAircraftID(int id){
    for(auto const aircraft:fleet){
        if(aircraft->getID()==id)
        return aircraft;
    }
    return nullptr;
}
std::string Airline::getID(){
    return ID;
}

#include"../Headers/Aircraft.h"
void Aircraft::setStatus(bool status){
isReadyForFlight=status;
}
void Aircraft::updateFuelLevel(int amount){
    fuelLevel=amount;
}

bool Aircraft::checkFlightStatus() const{
    return isReadyForFlight;
}
void Aircraft::assignFlight(Flight* newflight){
    if(newflight->getAircraftID()==this->ID){
    for(auto const flight:Flights){
        if(flight->getDate()==newflight->getDate()){
            std::cout<<"Can not be more then one flight per day";
        }
    }
    Flights.push_back(newflight);
    }else{
        std::cout<<"This flight for other plane";
    }
}
void Aircraft::boardPassenger(Passenger*newPassanger){
    if(capacity>passengers.size())
    passengers.push_back(newPassanger);
            else{
                std::cout<<"Plane is full of people";
            }
}
Aircraft::Aircraft(int Id,std::string Model,bool IsReadyForFlight,int FuelLevel,int Capacity){
    model=Model;isReadyForFlight=IsReadyForFlight;
    fuelLevel=FuelLevel;ID=Id;capacity=Capacity;
}
int Aircraft::getID(){
    return ID;
}
std::vector<Flight*> Aircraft::getFlights(){
    return Flights;
}
std::vector<Passenger*> Aircraft::getOfPlane(std::string place_name){
    std::vector <Passenger*> leavingPassengers;    
    if(!passengers.empty()){
    int amntOfPassengers=passengers.size();
    for(size_t i=0;i<amntOfPassengers;i++){
            if(place_name==passengers[i]->giveTicket()->getDestination()){
                    leavingPassengers.push_back(passengers[i]);
                    passengers.erase(passengers.begin()+i);
                    amntOfPassengers--;i--;
                }
            }
        return leavingPassengers; 
    }
    return leavingPassengers;
}
void Aircraft::fillWithFuel(){
    fuelLevel=100;
}
void Aircraft::useFuel(){
    fuelLevel-=10;
}

std::vector<Passenger*> Aircraft::getPassengers(){
return passengers;
}

int Aircraft::getFuel(){
return fuelLevel;
}


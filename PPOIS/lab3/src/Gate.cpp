#include"../Headers/Gate.h"
void Gate::addNewPassenger(Passenger* passenger){
for(auto const pass:passengerList){
    if(pass->showPassportID()==passenger->showPassportID()){
        std::cout<<"Passenger with such passport ID already exist";
        return;
    }
}
passengerList.push_back(passenger);
}
std::vector <Passenger*> Gate::passPassengers(){
    std::vector<Passenger*> passengersToPass;int amntOfPassengers=passengerList.size();
    if(amntOfPassengers!=0){
    for(size_t i=0;i<amntOfPassengers;i++){
        if(passengerList[i]->giveTicket()->getPlaneID()==expectedFlight->getAircraftID()){
            passengersToPass.push_back(passengerList[i]);
            passengerList.erase(passengerList.begin()+i);
            amntOfPassengers--;i--;
        }
    }
    return  passengersToPass;
    }
    else{
        std::cout<<"Queue is empty";
        return passengersToPass;
    }
}
void Gate::setFlight(Flight* flight){
 expectedFlight=flight;
}

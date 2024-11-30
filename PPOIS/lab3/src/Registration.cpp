#include"../Headers/Registration.h"
Ticket* Registration::soldTicket(std::string date,std::string destination,std::string name,std::string secondName,int passportID,int Class){
    std::vector<Flight*> flightsExactAirline; std::vector<int> passengers;
    for(auto const airline:*airlines){
        flightsExactAirline=airline->getFlightsForDestination(destination);
        for(auto const flight:flightsExactAirline){
            if(flight->getDate()==date){
                Ticket* tickt=new Ticket(date,airline->getID(),flight->getRunwayID(),airline->findAircraftID(flight->getAircraftID())->getID(),name,secondName,passportID,Class,destination);
                passengers=passengersByFlight[flight];
                passengers.push_back(passportID);
                passengersByFlight[flight]=passengers;
                return tickt;
            }
        }
    }
    return nullptr;
}

std::vector<Airline*>* Registration::getAirlines(){
    return airlines;
}

void Registration::cancelRegistration(Passenger* passenger,Ticket*& ticket){
    std::vector<int> passengers;
    for(auto const airline:*airlines){
       if(ticket->getAirlineID()==airline->getID()){
            for(auto const flight:airline->getFlightsForDestination(ticket->getDestination())){
                if(flight->getAircraftID()==ticket->getPlaneID()&&flight->getRunwayID()==ticket->getRunwayID()){
                    passengers=passengersByFlight[flight];
                    for(size_t i=0;i<passengers.size();i++){
                        if(passengers[i]==ticket->getPassportID()){
                            passengers.erase(passengers.begin()+i);
                            delete ticket; 
                            ticket = nullptr;
                             return;
                        }
                    }
                }
            }
        }
    }
    std::cout<<"The flight is out of date or the person is not registered"<<std::endl;
    }
    Registration::Registration(){
        airlines=new std::vector<Airline*>();
    }
    void Registration::add_airline(Airline* newAirline){
        for(auto const airline:*airlines){
            if(airline->getID()==newAirline->getID()){
                std::cout<<"Airline with such ID already exist";
                return;
            }
        }
        airlines->push_back(newAirline);
    }


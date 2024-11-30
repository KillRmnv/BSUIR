#include "../Headers/Passenger.h"
void Passenger::get_baggage_back(std::vector<Baggage*> checkedBaggage){
    baggageList=checkedBaggage;
}
std::vector<Baggage*> Passenger::giveBaggage(){
    return baggageList;
}
Ticket* Passenger::giveTicket(){
    if(ticket!=nullptr)
    return ticket;
    return new Ticket();
}
void Passenger::getTicket(Ticket* Ticket){
    ticket=Ticket;
}
int Passenger::showPassportID(){
return passportID;
}
Passenger::Passenger(int PassportID,std::string Name,std::string SecondName,int Age){
passportID=PassportID;name=Name;secondName=SecondName;age=Age;
}

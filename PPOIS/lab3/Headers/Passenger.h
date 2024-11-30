#pragma once

#include "Person.h"
#include "Ticket.h"
#include "Baggage.h"
#include <vector>
class Passenger:public Person{
private:
int passportID;
Ticket* ticket; 
std::vector<Baggage*> baggageList;
bool hasCheckedIn;
public:
using Person::Person;
Passenger()=default;
Passenger(int PassportID,std::string Name,std::string SecondName,int Age);
void get_baggage_back(std::vector<Baggage*> checkedBaggage);
std::vector<Baggage*> giveBaggage();
Ticket* giveTicket();
void getTicket(Ticket* Ticket);
int showPassportID();

};
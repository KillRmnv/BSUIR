#pragma once
#include"SysDate.h"
#include "AirportZone.h"
#include "Flight.h"
#include <iostream>
class Gate:AirportZone{
private:
Flight* expectedFlight;
int gateNum;
std::vector<Passenger*> passengerList;
bool validateTicket(Ticket* ticket);
public:
void addNewPassenger(Passenger* passenger);
std::vector <Passenger*> passPassengers();
Gate()=default;
Gate(Flight* ExpectedFlight,int Num):
expectedFlight(ExpectedFlight),gateNum(Num) {}
bool checkPassengerData(std::string name,std::string secondName,int passportID,Ticket* ticket);
void setFlight(Flight* flight);
};
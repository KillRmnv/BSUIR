#pragma once
#include"AirportZone.h"
#include<vector>
#include <iostream>
class SecurityCheckZone:AirportZone{
    private:
std::vector<Passenger*> queue;
public:
bool checkBaggage(std::vector<Baggage*> baggage,int Class);
void addPassenger(Passenger* passenger);
void DelPassenger();
int peopleInQueue();
};
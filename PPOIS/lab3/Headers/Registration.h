#pragma once
#include<iostream>
#include<vector>
#include"Airline.h"
#include "AirportZone.h"
#include<unordered_map>
class Registration:public AirportZone{
private:
std::vector<Airline*>* airlines;
std::unordered_map<Flight*,std::vector<int>> passengersByFlight;
public:
Ticket* soldTicket(std::string date,std::string destination,std::string name,std::string secondName,int PassportID,int Class);
std::vector<Airline*>* getAirlines();
void cancelRegistration(Passenger* passenger,Ticket*& ticket);
Registration();
void add_airline(Airline* newAirline);
};
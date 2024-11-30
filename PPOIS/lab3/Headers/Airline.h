#pragma once
#include <iostream>
#include <string>
#include<vector>
#include"Aircraft.h"
class Airline{
    private:
std::string name;
std::string ID;
std::vector<Aircraft*> fleet; 
std::vector<Flight*> destinations;
    public:
void addAircraft(Aircraft* aircraft);
void removeAircraft(Aircraft* aircraft,std::vector<Flight*>& toDistibute); 
std::vector<Aircraft*> getAvailableAircraft(std::string date) const;
std::vector<Flight*> getFlightsForDestination(const std::string& destination);
void scheduleFlight(Flight* flight);
Airline(std::string Name,std::string Id,std::vector<Aircraft*> Fleet, std::vector<Flight*> Destinations);
Airline()=default;
Aircraft* findAircraftID(int id);
std::string getID();
};
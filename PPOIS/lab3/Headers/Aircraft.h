#pragma once
#include<string>
#include "Vehicle.h"
#include "Flight.h"
#include "Passenger.h"
#include"Employee.h"
#include<vector>
#include "SysDate.h"
#include<iostream>
class Aircraft:public Vehicle{
private:
int ID;
std::string model;
bool isReadyForFlight;
int fuelLevel;
std::vector <Passenger*> passengers;
std::vector<Flight*> Flights;
public:
void setStatus(bool status);
void updateFuelLevel(int amount);
bool checkFlightStatus() const;
void assignFlight(Flight* newflight);
void boardPassenger(Passenger*newPassanger);
int getID();
std::vector<Flight*> getFlights();
Aircraft()=default;
Aircraft(int Id,std::string Model,bool IsReadyForFlight,int FuelLevel,int Capasity);
std::vector<Passenger*> getOfPlane(std::string place_name);
void fillWithFuel();
void useFuel();
int getFuel();
std::vector<Passenger*> getPassengers();
};
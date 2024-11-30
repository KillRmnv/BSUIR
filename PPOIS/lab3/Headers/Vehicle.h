#pragma once
#include<string>
class Vehicle{
    protected:
std::string registrationNumber;
std::string type;
bool isOperational;
int capacity; 
public:
void updateVehicleStatus( bool IsOperational);
};
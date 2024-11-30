#pragma once
#include <string>
class Ticket{
    private:
    std::string date;
    std::string airlineID;
    int RunwayID;
    int planeId; 
    std::string name;
    std::string secondName;
    std::string destination;
    int passportID;
    int Class;
public:
Ticket(std::string Date,std::string AirlineID,int runwayID,int PlaneId, std::string Name,std::string SecondName,int PassportID,int Clas,std::string Destination);
std::string getName();
std::string getSecondName();
int getPlaneID();
std::string getDate();
std::string getDestination();
std::string getAirlineID();
int getRunwayID();
int getPassportID();
Ticket();
};

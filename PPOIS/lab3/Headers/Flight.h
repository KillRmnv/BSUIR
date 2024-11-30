#pragma once
#include<string>
class Flight{
    private:
    std::string date;
    int aircraftID;
    int runwayID;
    bool status;
    std::string airline;
    std::string destination;
    public:
    void cancelFlight();
    bool getStatus();
    Flight(std::string Date,int AircraftId,int runway,std::string Airline,std::string Destination);
    Flight()=default;
    std::string getDate();
    std::string getDestination();
    int getAircraftID();
    std::string getAirline();
    int getRunwayID();

};
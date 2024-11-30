#include"../Headers/Flight.h"
    void Flight::cancelFlight(){
        status=false;
    }
    bool Flight::getStatus(){
        return status;
    }
    Flight::Flight(std::string Date,int AircraftId,int runway,std::string Airline,std::string Destination){
        date=Date;aircraftID=AircraftId;runwayID=runway;airline=Airline;destination=Destination;
    }
    
    std::string Flight::getDate(){
        return date;
    }
    std::string Flight::getDestination(){
        return destination;
    }
        int Flight::getAircraftID(){
            return aircraftID;
    }
        int Flight::getRunwayID(){
           return runwayID; 
    }

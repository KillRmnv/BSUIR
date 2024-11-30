#include"../Headers/Ticket.h"
Ticket::Ticket(std::string Date,std::string AirlineID,int runwayID,int PlaneId, std::string Name,std::string SecondName,int PassportID,int Clas,std::string Destination){
date=Date;airlineID=AirlineID;RunwayID=runwayID;planeId=PlaneId;name=Name;secondName=SecondName;passportID=PassportID;Class=Clas;destination=Destination;
}
std::string Ticket::getName(){
return name;
}
std::string Ticket::getSecondName(){
return secondName;
}
int Ticket::getPlaneID(){
return planeId;
}
std::string Ticket::getDate(){
return date;
}
std::string Ticket::getDestination(){
return destination;
}
std::string Ticket::getAirlineID(){
return airlineID;
}
int Ticket::getRunwayID(){
return RunwayID;
}
int Ticket::getPassportID(){
return passportID;
}
Ticket::Ticket(){
    RunwayID=0;planeId=0;passportID=0;
}
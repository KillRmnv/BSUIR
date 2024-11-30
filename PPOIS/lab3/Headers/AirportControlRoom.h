#include "Aircraft.h"
#include "AirportZone.h"
#include "Runway.h"
#include"SysDate.h"
class AirportControlRoom:public AirportZone{
private:
std::vector<Runway*> runways;
std::string location;
public:
void recieveAircraft(Aircraft* newOne);
Aircraft* sendAircraft();
void addRunway(Runway* newOne);
AirportControlRoom()=default;
AirportControlRoom(std::string Location,std::vector<Runway*> Runways);
};
#include "MaintenanceService.h"
#include "Registration.h"
#include "AirportControlRoom.h"
#include "SecurityCheckZone.h"
class Airport{
    private:
    std::string location;
    AirportControlRoom* controlRoom;
    MaintenanceService* service;
    Registration* registration;
    SecurityCheckZone* security;
    public:
     Airport(const std::string& loc, AirportControlRoom* ctrl, MaintenanceService* srv,
    Registration* reg, SecurityCheckZone* sec);
    ~Airport();
    AirportControlRoom* getControlRoom();
    MaintenanceService* getService();
    Registration* getRegistration();
    SecurityCheckZone* getSecurity();
    std::string getLocation();
};
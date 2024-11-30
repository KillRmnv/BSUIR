#include "../Headers/Airport.h"

Airport::Airport(const std::string& loc, AirportControlRoom* ctrl, MaintenanceService* srv,
                 Registration* reg, SecurityCheckZone* sec)
    : location(loc), controlRoom(ctrl), service(srv), registration(reg), security(sec) {}

Airport::~Airport() {
    delete controlRoom;
    delete service;
    delete registration;
    delete security;
}

AirportControlRoom* Airport::getControlRoom() {
    return controlRoom;
}

MaintenanceService* Airport::getService() {
    return service;
}

Registration* Airport::getRegistration() {
    return registration;
}

SecurityCheckZone* Airport::getSecurity() {
    return security;
}

std::string Airport::getLocation() {
    return location;
}

#pragma once

#include <string>
#include <vector>
#include "Passenger.h"

class AirportZone{
protected:
int zoneID; 
bool stateofWork;
public:
bool get_state_of_work();
void set_state_of_work(bool state);
int get_ID();
AirportZone()=default;
AirportZone(int zone,bool state):
zoneID(zone),stateofWork(state){}
};
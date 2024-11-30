#include"../Headers/AirportZone.h"
bool AirportZone::get_state_of_work(){
return stateofWork;
}
void AirportZone::set_state_of_work(bool state){
stateofWork=state;
}
int AirportZone::get_ID(){
return zoneID;
}
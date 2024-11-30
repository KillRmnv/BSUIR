#include "../Headers/Baggage.h"
void Baggage::updateBaggageStatus(bool checkedIn){
isCheckedIn=checkedIn;
}
bool Baggage::isBaggageCheckedIn() const{
return isCheckedIn;
}
int Baggage::get_weight(){
return weight;
}
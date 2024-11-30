#pragma once
#include <string>
class Baggage{
private:
int baggageID;
double weight; 
bool isCheckedIn;
int type;
public:
void updateBaggageStatus(bool checkedIn); 
bool isBaggageCheckedIn() const; 
int get_weight();
Baggage()=default;
Baggage(int ID,double Wheight,int Type):
baggageID(ID),weight(Wheight),isCheckedIn(false),type(Type){}
};
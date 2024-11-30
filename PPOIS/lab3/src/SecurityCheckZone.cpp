#include"../Headers/SecurityCheckZone.h"
void SecurityCheckZone::DelPassenger(){
    if(!queue.empty()){
Passenger* toDelete=queue[queue.size()-1];
queue.erase(queue.begin()+(queue.size()-1));
delete toDelete;
return;
    }
}

bool SecurityCheckZone::checkBaggage(std::vector<Baggage*> baggage,int Class){
    int wheight=0;
    for(auto const bag:baggage){
        wheight+=bag->get_weight();
    }
    if(Class==1&&wheight>32)
    return false;
    if(Class==2&&wheight>20)
    return false;
    return true;
}
void SecurityCheckZone::addPassenger(Passenger* passenger){
    for(auto const passengerInQueue:queue){
        if(passengerInQueue->showPassportID()==passenger->showPassportID()){
            std::cout<<"Passenger with such passport ID already in queue";
            return;
        }
    }
    queue.push_back(passenger);
}
int SecurityCheckZone::peopleInQueue(){
    return queue.size();
}

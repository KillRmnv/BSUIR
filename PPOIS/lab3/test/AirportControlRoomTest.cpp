#include <gtest/gtest.h>
#include "../Headers/AirportControlRoom.h"
#include "../Headers/Aircraft.h"
#include "../Headers/Runway.h"
#include "../Headers/SysDate.h"




TEST(AirportControlRoomTest, RecieveAircraft) {
    SysDate sysDate;
    Runway* runway1=new Runway(2);
    Runway* runway2=new Runway(3);
   std::vector<Runway*> runWays;
   runWays.push_back(runway1);
    runWays.push_back(runway2);
    AirportControlRoom controlRoom("NYC",runWays);

    Aircraft* aircraft=new Aircraft(3,"Kukuruznik",true,100,2);
    Flight* newOne=new Flight(sysDate.getSysDate(),3,2,"Eco","NYC");
    aircraft->assignFlight(newOne);

    controlRoom.recieveAircraft(aircraft);

    EXPECT_TRUE(runWays[0]->getStatus() || runWays[1]->getStatus());
    EXPECT_EQ(runWays[0]->getAircraft()->getID(), aircraft->getID());
    delete runway1;delete runway2;delete aircraft;delete newOne;
}

TEST(AirportControlRoomTest, SendAircraft) {
    SysDate sysDate;
    std::vector<Runway*> runways;
    Runway* runway=new Runway(2);
    ServiceCar* baggageCar = new ServiceCar("Baggage");
    runway->setBaggageCar(baggageCar);
    ServiceCar* fuelCar = new ServiceCar("Fuel");
    runway->setFuelCar(fuelCar);
    runways.push_back(runway);
    AirportControlRoom controlRoom("New York",runways);

    Aircraft* aircraft=new Aircraft(432,"tyu",true,90,100);
        Flight* flight2=new Flight(sysDate.getSysDate(),432,2,"ChooseLife","Los Angeles");
    aircraft->assignFlight(flight2);
    runway->landPlane(aircraft, "New York");

    Aircraft* sentAircraft = controlRoom.sendAircraft();
    EXPECT_EQ(sentAircraft->getID(), aircraft->getID());

    aircraft->updateFuelLevel(5); 
    controlRoom.sendAircraft();
    EXPECT_GT(aircraft->getFuel(), 5); 
}

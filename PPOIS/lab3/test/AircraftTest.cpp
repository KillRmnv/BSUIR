#include "gtest/gtest.h"
#include "../Headers/Aircraft.h"


TEST(AircraftTest, ConstructorTest) {
    Aircraft aircraft(432, "Boeing 737", true, 50,5);
    EXPECT_EQ(aircraft.getID(), 432);
    EXPECT_EQ(aircraft.checkFlightStatus(), true);
    EXPECT_EQ(aircraft.getFuel(), 50);
}

TEST(AircraftTest, SetStatusTest) {
    Aircraft aircraft;
    aircraft.setStatus(false);
    EXPECT_EQ(aircraft.checkFlightStatus(), false); 
}

TEST(AircraftTest, UpdateFuelLevelTest) {
    Aircraft aircraft;
    aircraft.updateFuelLevel(80);
    EXPECT_EQ(aircraft.getFuel(), 80);
}

TEST(AircraftTest, FillWithFuelTest) {
    Aircraft aircraft;
    aircraft.fillWithFuel();
    EXPECT_EQ(aircraft.getFuel(), 100);
}

TEST(AircraftTest, UseFuelTest) {
    Aircraft aircraft(1, "Airbus A320", true, 50,3);
    aircraft.useFuel();
    EXPECT_EQ(aircraft.getFuel(), 40);
}

TEST(AircraftTest, BoardPassengerTest) {
    Aircraft aircraft;
    Passenger passenger("Marelyn","Manson",25);
    aircraft.boardPassenger(&passenger);
    auto passengers = aircraft.getPassengers(); 
    EXPECT_EQ(passengers.size(), 1);
    EXPECT_EQ(passengers[0]->sayName(), "Marelyn");
}

TEST(AircraftTest, AssignFlightTest) {
    Aircraft aircraft(432,"Boing",false,89,100);
    Flight flight1( "2024-11-30",432,3,"ChooseLife","New York");
    Flight flight2("2024-11-30",432,3,"ChooseLife","Los Angeles");

        aircraft.assignFlight(&flight1);
    EXPECT_EQ(aircraft.getFlights().size(), 1);
        testing::internal::CaptureStdout();
    aircraft.assignFlight(&flight2);
        std::string output = testing::internal::GetCapturedStdout();

    EXPECT_EQ(output, "Can not be more then one flight per day");
}

TEST(AircraftTest, GetOfPlaneTest) {
    Aircraft aircraft;

    Passenger* passenger1=new Passenger(234567,"Alice","Marlow",23);
    passenger1->getTicket(new Ticket("2024-12-31","ChooseLife",3,432,"Alice","Marlow",234567,1,"Paris"));
    Passenger* passenger2=new Passenger(11992288,"Bob","Marley",45);
    passenger2->getTicket(new Ticket("2024-12-31","ChooseLife",3,432,"Bob","Marley",11992288,1,"Paris"));
    Passenger* passenger3=new Passenger(567392,"Charlie", "Chaplin",38);
    passenger3->getTicket(new Ticket("2024-12-31","ChooseLife",3,432,"Bob","Marley",11992288,1,"London"));

    aircraft.boardPassenger(passenger1);
    aircraft.boardPassenger(passenger2);
    aircraft.boardPassenger(passenger3);

    auto leavingPassengers = aircraft.getOfPlane("Paris");
    EXPECT_EQ(leavingPassengers.size(), 2);
    EXPECT_EQ(leavingPassengers[0]->sayName(), "Alice");
    EXPECT_EQ(leavingPassengers[1]->sayName(), "Bob");
    EXPECT_EQ(aircraft.getPassengers().size(), 1); // Остался только Charlie
}

TEST(AircraftTest, BoardPassengerCapacityTest) {
    Aircraft aircraft(1, "Boeing 737", true, 50,2);
    Passenger *passenger1;
    Passenger *passenger2;
    Passenger* passenger3;

    aircraft.boardPassenger(passenger1);
    aircraft.boardPassenger(passenger2);
            testing::internal::CaptureStdout();
                aircraft.boardPassenger(passenger3);
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"Plane is full of people");
}


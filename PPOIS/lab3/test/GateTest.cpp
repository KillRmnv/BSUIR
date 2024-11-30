#include "../Headers/Gate.h"
#include "../Headers/Passenger.h"
#include "../Headers/Flight.h"
#include "../Headers/Ticket.h"
#include <gtest/gtest.h>

TEST(GateTests, AddNewPassenger_NoDuplicates) {
    Gate gate;
    Passenger* passenger1 = new Passenger(12345, "John", "Doe", 30);
    Passenger* passenger2 = new Passenger(12345, "Jane", "Doe", 25); 
    
    gate.addNewPassenger(passenger1);
     testing::internal::CaptureStdout();
    gate.addNewPassenger(passenger2);
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"Passenger with such passport ID already exist");
   

    delete passenger1;
    delete passenger2;
}

TEST(GateTests, AddNewPassenger_UniquePassengers) {
    Gate gate;
        Flight* expectedOne=new Flight( "2024-11-30",432,3,"ChooseLife","New York");
    Ticket* ticket1=new Ticket("2024-11-31","ChooseLiFe",3,342,"John","Johnsone",12345,2,"NYC");
    Ticket* ticket2=new Ticket("2024-11-31","ChooseLiFe",3,342,"John","Johnsone",67890,2,"NYC");
    Passenger* passenger1 = new Passenger(12345, "John", "Johnsone", 30);
    passenger1->getTicket(ticket1);
    Passenger* passenger2 = new Passenger(67890, "Jane", "Mary", 25);
    passenger2->getTicket(ticket2);
    gate.addNewPassenger(passenger1);
    gate.addNewPassenger(passenger2);
    gate.setFlight(expectedOne);

    EXPECT_EQ(gate.passPassengers().size(), 0); 

    delete passenger1;
    delete passenger2;
}

TEST(GateTests, PassPassengers_MatchingFlight) {
    Flight* expectedFlight=new Flight("2024-12-01", 101, 3, "AirlineA", "New York");
    Gate gate(expectedFlight,3);

    Ticket* ticket1 = new Ticket("2024-12-01","AirlineA",3,101,"Joe","Rogan",12345,1,"New York"); // совпадает рейс
    Ticket* ticket2 = new Ticket("2024-12-02","AirlineA",3,102,"Joe","Rogan",12345,1,"New York"); // не совпадает рейс

    Passenger* passenger1 = new Passenger(12345, "Joe", "Rogan", 30);
    Passenger* passenger2 = new Passenger(67890, "Jane", "Doe", 25);

    passenger1->getTicket(ticket1);
    passenger2->getTicket(ticket2);

    gate.addNewPassenger(passenger1);
    gate.addNewPassenger(passenger2);

    auto passedPassengers = gate.passPassengers();

    ASSERT_EQ(passedPassengers.size(), 1);
    EXPECT_EQ(passedPassengers[0]->showPassportID(), 12345);

    auto remainingPassengers = gate.passPassengers();
    EXPECT_EQ(remainingPassengers.size(), 0); 

    delete passenger1;
    delete passenger2;
    delete ticket1;
    delete ticket2;
}

TEST(GateTests, PassPassengers_NoPassengers_ThrowsException) {
    Flight* expectedFlight=new Flight("2024-12-01", 101, 3, "AirlineA", "New York");
    Gate gate(expectedFlight,3);
    testing::internal::CaptureStdout();
        gate.passPassengers();
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"Queue is empty");
}
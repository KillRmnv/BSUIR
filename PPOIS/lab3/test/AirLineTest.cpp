#include <gtest/gtest.h>
#include "../Headers/Airline.h"


TEST(AirlineTest, ConstructorAndGetID) {
    Airline airline("AirlineName", "AL123", {}, {});
    EXPECT_EQ(airline.getID(), "AL123");
}

TEST(AirlineTest, AddAircraft) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft aircraft1(1, "Boeing 747", true, 100,10);

    airline.addAircraft(&aircraft1);
    EXPECT_EQ(airline.getAvailableAircraft("2024-11-25").size(), 1);
}

TEST(AirlineTest, RemoveAircraft) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft* aircraft1=new Aircraft(1, "Boeing 747", true, 100,10);
    Aircraft* aircraft2=new Aircraft(2, "Airbus A320", true, 90,10);
    Flight* flight1=new Flight( "2024-11-30",1,3,"ChooseLife","New York");
    std::vector<Flight*> redistributedFlights;
    aircraft1->assignFlight(flight1);
    airline.addAircraft(aircraft1);
    airline.addAircraft(aircraft2);
    

    airline.removeAircraft(aircraft1, redistributedFlights);
    EXPECT_EQ(redistributedFlights.size(), 1); // Рейс должен быть перераспределен
    EXPECT_EQ(airline.getAvailableAircraft("2024-11-30").size(), 1); // Один самолет остался
}

TEST(AirlineTest, GetAvailableAircraft) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft aircraft1(1, "Boeing 747", true, 100,10);
    Aircraft aircraft2(2, "Airbus A320", true, 90,10);
    Flight* flight1=new Flight( "2024-11-30",1,3,"ChooseLife","New York");

    aircraft1.assignFlight(flight1);
    airline.addAircraft(&aircraft1);
    airline.addAircraft(&aircraft2);

    auto availableAircraft = airline.getAvailableAircraft("2024-11-30");
    EXPECT_EQ(availableAircraft.size(), 1); // Один самолет свободен
    EXPECT_EQ(availableAircraft[0]->getID(), 2); // Свободен Airbus A320
}

TEST(AirlineTest, GetFlightsForDestination) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft aircraft1(1, "Boeing 747", true, 100,10);
    Aircraft aircraft2(2, "Airbus A320", true, 90,10);
    airline.addAircraft(&aircraft1);
    airline.addAircraft(&aircraft2);
    Flight* flight1=new Flight("2024-11-25",1,4,"ChooseFamily","LAX");
    Flight* flight2=new Flight("2024-12-01",2,3,"ChooseJob", "SFO");
    Flight* flight3=new Flight("2024-12-05", 1,1,"ChooseLife", "SFO");

    airline.scheduleFlight(flight1);
    airline.scheduleFlight(flight2);
    airline.scheduleFlight(flight3);

    auto flightsToLAX = airline.getFlightsForDestination("LAX");
    EXPECT_EQ(flightsToLAX.size(), 1);
    EXPECT_EQ(flightsToLAX[0]->getDestination(), "LAX");

    auto flightsToSFO = airline.getFlightsForDestination("SFO");
    EXPECT_EQ(flightsToSFO.size(), 2);
}

TEST(AirlineTest, ScheduleFlight) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft aircraft1(1, "Boeing 747", true, 100,7);
    Flight* flight1=new Flight("2024-11-25",1,4,"ChooseFamily","LAX");

    airline.addAircraft(&aircraft1);
    airline.scheduleFlight(flight1);

    EXPECT_EQ(aircraft1.getFlights().size(), 1);
    EXPECT_EQ(aircraft1.getFlights()[0]->getDestination(), "LAX");
}

TEST(AirlineTest, FindAircraftID) {
    Airline airline("TestAirline", "AL123", {}, {});
    Aircraft aircraft1(1, "Boeing 747", true, 100,23);
    Aircraft aircraft2(2, "Airbus A320", true, 90,45);

    airline.addAircraft(&aircraft1);
    airline.addAircraft(&aircraft2);

    Aircraft* foundAircraft = airline.findAircraftID(2);
    ASSERT_NE(foundAircraft, nullptr);
    EXPECT_EQ(foundAircraft->getID(), 2);

    Aircraft* notFoundAircraft = airline.findAircraftID(3);
    EXPECT_EQ(notFoundAircraft, nullptr);
}

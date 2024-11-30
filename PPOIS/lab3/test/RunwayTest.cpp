#include "../Headers/Runway.h"
#include "../Headers/Aircraft.h"
#include "../Headers/ServiceCar.h"
#include <gtest/gtest.h>

TEST(RunwayTests, ConstructorTest) {
    Runway runway(1);
    EXPECT_EQ(runway.getStatus(), false); 
}

TEST(RunwayTests, SetNewAircraftTest) {
    Runway runway(1);
    Aircraft* aircraft = new Aircraft(101, "Boeing 737", true, 100, 200);

    runway.setNewAircraft(aircraft);

    EXPECT_EQ(runway.getAircraft(), aircraft);
    EXPECT_EQ(runway.getStatus(), true);

    delete aircraft;
}

TEST(RunwayTests, UpdateStatusTest) {
    Runway runway(1);

    runway.updateStatus(true);
    EXPECT_EQ(runway.getStatus(), true);

    runway.updateStatus(false);
    EXPECT_EQ(runway.getStatus(), false);
}

TEST(RunwayTests, LandPlaneTest) {
    Runway runway(1);
    Aircraft* aircraft = new Aircraft(102, "Airbus A320", true, 80, 180);

    std::string location = "Terminal A";

    runway.landPlane(aircraft, location);

    EXPECT_EQ(runway.getAircraft()->getID(), aircraft->getID());
    EXPECT_EQ(runway.getStatus(), true);

    EXPECT_FALSE(aircraft->checkFlightStatus());

    delete aircraft;
}


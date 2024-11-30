#include "../Headers/SecurityCheckZone.h"
#include "../Headers/Passenger.h"
#include "../Headers/Baggage.h"
#include <gtest/gtest.h>

TEST(SecurityCheckZoneTests, AddPassengerTest) {
    SecurityCheckZone securityZone;
    Passenger* passenger1 = new Passenger(123, "John", "Doe", 30);
    Passenger* passenger2 = new Passenger(124, "Jane", "Doe", 25);

    EXPECT_NO_THROW(securityZone.addPassenger(passenger1)); // Добавление первого пассажира
    EXPECT_NO_THROW(securityZone.addPassenger(passenger2)); // Добавление второго пассажира

    Passenger* duplicatePassenger = new Passenger(123, "Duplicate", "Doe", 35);
      testing::internal::CaptureStdout();
    securityZone.addPassenger(duplicatePassenger);
        std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output,"Passenger with such passport ID already in queue");

    delete passenger1;
    delete passenger2;
    delete duplicatePassenger;
}


TEST(SecurityCheckZoneTests, CheckBaggageTest) {
    SecurityCheckZone securityZone;

    Baggage* bag1 = new Baggage(1, 15.0, 1);
    Baggage* bag2 = new Baggage(2, 10.0, 1); 
    std::vector<Baggage*> baggage = {bag1, bag2};

    EXPECT_TRUE(securityZone.checkBaggage(baggage, 1));
    EXPECT_FALSE(securityZone.checkBaggage(baggage, 2)); 

    delete bag1;
    delete bag2;
}

TEST(SecurityCheckZoneTests, DelPassengerTest) {
    SecurityCheckZone securityZone;
    Passenger* passenger1 = new Passenger(123, "John", "Doe", 30);
    Passenger* passenger2 = new Passenger(124, "Jane", "Doe", 25);

    securityZone.addPassenger(passenger1);
    securityZone.addPassenger(passenger2);

    EXPECT_EQ(securityZone.peopleInQueue(),2);
    securityZone.DelPassenger();
    EXPECT_EQ(securityZone.peopleInQueue(),1);
    securityZone.DelPassenger();
    EXPECT_EQ(securityZone.peopleInQueue(),0);
}

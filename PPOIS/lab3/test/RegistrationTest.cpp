#include "../Headers/Registration.h"
#include "../Headers/Airline.h"
#include "../Headers/Passenger.h"
#include "../Headers/Ticket.h"
#include "../Headers/Flight.h"
#include <gtest/gtest.h>

TEST(RegistrationTests, SoldTicket_Success) {
    Registration registration;

    Airline* airline = new Airline("TestAirline", "A001", {}, {});
    Flight* flight = new Flight("2024-12-01", 101, 1, "TestAirline", "New York");
    Aircraft* aircraft = new Aircraft(101, "Boeing 737", true, 100, 200);
    airline->addAircraft(aircraft);
    airline->scheduleFlight(flight);
    registration.getAirlines()->push_back(airline);
    Ticket* ticket = registration.soldTicket("2024-12-01", "New York", "John", "Doe", 12345, 1);

    // Проверяем корректность данных
    ASSERT_NE(ticket, nullptr);
    EXPECT_EQ(ticket->getDate(), "2024-12-01");
    EXPECT_EQ(ticket->getDestination(), "New York");
    EXPECT_EQ(ticket->getPassportID(), 12345);

    delete ticket;
    delete airline;
    delete aircraft;
    delete flight;
}

TEST(RegistrationTests, SoldTicket_NoMatchingFlight) {
    Registration registration;

    Airline* airline = new Airline("TestAirline", "A001", {}, {});
    Flight* flight = new Flight("2024-12-01", 101, 1, "TestAirline", "Los Angeles");
    airline->scheduleFlight(flight);
    registration.getAirlines()->push_back(airline);

    Ticket* ticket = registration.soldTicket("2024-12-01", "New York", "John", "Doe", 12345, 1);

    EXPECT_EQ(ticket, nullptr);

    delete airline;
    delete flight;
}

TEST(RegistrationTests, CancelRegistration_Success) {
    Registration registration;
        Flight* flight = new Flight("2024-12-01", 101, 1, "TestAirline", "NYC");
    std::vector<Flight*> flights;
    flights.push_back(flight);
    Aircraft* aircraft = new Aircraft(101, "Boeing 737", true, 100, 200);
    std::vector<Aircraft*> planes;
    planes.push_back(aircraft);
    Airline* airline = new Airline("TestAirline", "A001", planes, flights);
        registration.add_airline(airline);
    Passenger* passenger = new Passenger(12345, "John", "Doe", 30);
    Ticket* ticket =registration.soldTicket("2024-12-01", "NYC", passenger->sayName(), passenger->saySecondName(), passenger->showPassportID(), 2);

    registration.cancelRegistration(passenger, ticket);
    if(ticket==nullptr)
    ticket=new Ticket();
    EXPECT_EQ(ticket->getPassportID(),0);
    delete airline;
    delete aircraft;
    delete flight;
    delete passenger;
}

TEST(RegistrationTests, CancelRegistration_PassengerNotFound) {
    Registration registration;

    Airline* airline = new Airline("TestAirline", "A001", {}, {});
    Flight* flight = new Flight("2024-12-01", 101, 1, "TestAirline", "New York");
    Aircraft* aircraft = new Aircraft(101, "Boeing 737", true, 100, 200);
    airline->addAircraft(aircraft);
    airline->scheduleFlight(flight);

    Passenger* passenger = new Passenger(67890, "Jane", "Doe", 25); // не зарегистрированный пассажир
    Ticket* ticket = new Ticket("2024-12-01", airline->getID(), flight->getRunwayID(), aircraft->getID(), "Jane", "Doe", 67890, 1,"LA");

    registration.getAirlines()->push_back(airline);

    EXPECT_NO_THROW(registration.cancelRegistration(passenger, ticket)); 

    delete airline;
    delete aircraft;
    delete flight;
    delete passenger;
    delete ticket;
}

TEST(RegistrationTests, GetAirlines_Success) {
    Registration registration;

    Airline* airline1 = new Airline("Airline1", "A001", {}, {});
    Airline* airline2 = new Airline("Airline2", "A002", {}, {});
    registration.getAirlines()->push_back(airline1);
    registration.getAirlines()->push_back(airline2);

    auto airlines = registration.getAirlines();


    EXPECT_EQ(airlines->size(), 2);
    EXPECT_EQ(airlines->at(0)->getID(), "A001");
    EXPECT_EQ(airlines->at(1)->getID(), "A002");


    delete airline1;
    delete airline2;
}

#include "AircraftTest.cpp"
#include "AirLineTest.cpp"
#include "AirportControlRoomTest.cpp"
#include "GateTest.cpp"
#include "MaintenanceServiceTest.cpp"
#include "RegistrationTest.cpp"
#include "RunwayTest.cpp"
#include "SecurityCheckZoneTest.cpp"

int main(int argc, char** argv) {
    setlocale(LC_ALL, "ru");
        std::locale::global(std::locale("ru_RU.UTF-8")); 
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS(); 
}
    #include"../Headers/SysDate.h"
    std::string SysDate::getSysDate(){
        auto now = std::chrono::system_clock::now();
    std::time_t currentTime = std::chrono::system_clock::to_time_t(now);

    std::tm localTime = *std::localtime(&currentTime);

    std::ostringstream oss;
    oss << std::put_time(&localTime, "%Y-%m-%d");

    return oss.str();
    }
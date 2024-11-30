#include "../src/Employee.h"
inline int Employee::get_department() {
    return Department;
}

inline std::string Employee::to_string() {
    return position;
}

 nlohmann::json Employee::to_json() {
    nlohmann::json pos;
    pos["position"] = position;
    pos["Department"] = Department;
    return pos;
}


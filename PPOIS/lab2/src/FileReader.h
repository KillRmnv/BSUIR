#pragma once
#include <nlohmann/json.hpp>
#include <fstream>
#include "Employee.h"
#include "EDocument.h"
#include "EDocument.h"
#include "Storage.h"
class FileReader{
    private:
    public:
    nlohmann::json build(std::string object_name);
};
#pragma once
#include <nlohmann/json.hpp>
#include <fstream>
#include "Employee.h"
#include "Document.h"
#include "Storage.h"
class FileWriter{
    public:
    void rewrite(nlohmann::json documents,std::string storage_name);
};

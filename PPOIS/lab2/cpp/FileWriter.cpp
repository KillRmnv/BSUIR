#include "../src/FileWriter.h"
    void FileWriter::rewrite(nlohmann::json documents,std::string storage_name){
    storage_name+=".json";
    std::ofstream file(storage_name);
    if(!documents.empty())
    file<<documents;
    file.close();
}
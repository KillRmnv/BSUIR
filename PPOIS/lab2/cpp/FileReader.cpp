#include "../src/FileReader.h"
 nlohmann::json FileReader::build(std::string object_name){
    object_name+=".json";
    nlohmann::json doc=nlohmann::json::array();
    std::ifstream file(object_name);
     if (!file.is_open()) {
         std::ofstream created_file(object_name, std::ios::app);
         created_file.close();
         std::cout<<object_name<<" created"<<std::endl;
    }else{
    file.seekg(0, std::ios::end);
    long size = file.tellg(); 
    if(size!=0)
    file>>doc;
    file.close();
    }
    return doc;
   }
#pragma once
#include <unordered_map>
#include "EDocument.h"
#include<string>
#include<vector>
#include <nlohmann/json.hpp>
#include<iostream>
#include"FileWriter.h"
class Storage{
protected:
std::unordered_map<std::string, std::vector<int>> indexByAuthor;
std::unordered_map<std::string, std::vector<int>> indexByDate;
std::unordered_map<std::string, std::vector<int>> indexByType;
std::unordered_map<int, std::vector<int>> indexByID;
nlohmann::json documents=nlohmann::json::array();
public:
 Storage& del_exact_doc(std::string storage_name,int id);
 Storage& add_document(nlohmann::json new_doc,std::string storage_name);
 Storage(nlohmann::json docs_from_file);
 Storage(){};
 nlohmann::json to_json();
 bool check_for_existance(int id);
 Storage& del_doc(Document doc,std::string storage_name);
 EDocument find_doc(int id);
 bool is_empty();
};

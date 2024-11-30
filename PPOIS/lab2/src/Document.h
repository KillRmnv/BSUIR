#pragma once

#include<string>
#include"Comment.h"
#include"RevisionHistory.h"
#include <vector>
#include <nlohmann/json.hpp>
#include <iostream>
class Document{
    protected:
    std::string type;
    std::string name;
    int ID=0;
    std::string creation_date;
    std::string author;
    std::string expiry_date;
    bool signature;
    bool stamp;
    RevisionHistory history;
    public:
     virtual ~Document() = default; 
        nlohmann::json to_json() const ;
       static Document from_json( const nlohmann::json j);
    Document(std::string Type,std::string Name,int id,std::string Creation_date,std::string Author,std::string Expiry_date,
    bool Signature,bool Stamp,RevisionHistory History): type(Type),name(Name),ID(id),creation_date(Creation_date),author(Author),expiry_date(Expiry_date),
    signature(Signature),stamp(Stamp),history(History) {}
    int get_ID();
    void info_about_document();
    Document(){};
    int get_date_int();
    std::string get_author();
    std::string get_date();
    std::string get_type();
    std::string get_name();
       void Display(int num);
       bool operator==( Document& other)  ;
       std::string get_creation_date();
       std::string get_expiry_date();
       bool is_stamped();
       bool is_signed();
};
#pragma once


#include"EDocument.h"
#include"FileReader.h"
#include "Administrator.h"
#include"Bookkeeper.h"
#include "FinManager.h"
#include "Lawyer.h"
#include "DocsList.h"
#include "Notification.h"
#include "ActivityLog.h"




class Personal_account{
    private:
    Employee* position=nullptr;
    DocsList ToDoDocs;
    std::vector<Notification> receipts;
    ActivityLog user_history;
    EDocument current_doc;
    public:
     ActivityLog& get_log() ;
    nlohmann::json to_json() const;
    static Personal_account from_json(nlohmann::json json_file);
    EDocument choose_from_list(int num);
    void updateToDoList(EDocument doc);
    int amnt_of_docs();
    DocsList& get_list();
    Personal_account(){}
     void Identify_position(std::string Position);
    void add_notifaction(Notification& new_one);
    void set_doc(EDocument doc);
   Employee* get_position();
   EDocument copy();
   void Display();
   Personal_account(std::string Position_line);
   EDocument create_doc(int user_ID,std::string type,std::string name,int id, std::string creation_date, std::string author,
 std::string expiry_date, SystemDate date,   std::string file_path);
   std::vector<Notification> get_notifications();
   bool has_document(int id);
};



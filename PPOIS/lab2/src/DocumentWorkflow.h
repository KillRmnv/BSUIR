#pragma once

#include "EDocument.h"
#include "Personal_account.h"
#include "Storage.h"
#include "Department.h"
#include "SystemDate.h"
#include<nlohmann/json.hpp>


class DocumentWorkflow{
    private:
    Department administration;
    Department HR;
    Department finances;
    Department bookkeeping;
    Department Legal;
    Storage ActiveDocuments;
    Storage ArchiveDocuments;
    public:
    void from_json(nlohmann::json users,nlohmann::json active_storage,nlohmann::json archive);
    nlohmann::json to_json();
    void add_to_archive(Document archive_doc);
    void add_to_storage(Document doc);
    void add_user(User user);
    void del_user(User user);
    void del_from_storage(int doc_id);
    void del_from_archive(Document doc);
    void del_from_storage(Document doc);
    User find_user(int ID);
    Storage& get_storage();
    void move_from_storage_to_archive(Document  doc,User user,int amnt);
    void distribute_doc(int Department,EDocument doc,int amnt,User user);



    Storage get_archive();
};
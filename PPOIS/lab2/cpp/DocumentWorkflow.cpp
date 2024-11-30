#include "../src/DocumentWorkflow.h"

    void DocumentWorkflow::move_from_storage_to_archive(Document  doc,User user ,int amnt){
        add_to_archive(doc);
        del_from_storage(doc);
    }
  void DocumentWorkflow::from_json(nlohmann::json users, nlohmann::json active_storage, nlohmann::json archive) {
    if(!users.empty()){
        administration = Department::from_json_users(users.at("administration"));
        HR = Department::from_json_users(users.at("HR"));
        finances = Department::from_json_users(users.at("finances"));
        bookkeeping = Department::from_json_users(users.at("bookkeeping"));
        Legal = Department::from_json_users(users.at("Legal"));
    }
    if(!active_storage.empty())
        ActiveDocuments = Storage(active_storage);
        if(!archive.empty())
        ArchiveDocuments = Storage(archive);
    }

    nlohmann::json DocumentWorkflow::to_json() {
        nlohmann::json json_file;

        json_file["administration"] = administration.to_json_users();
        json_file["HR"] = HR.to_json_users();
        json_file["finances"] = finances.to_json_users();
        json_file["bookkeeping"] = bookkeeping.to_json_users();
        json_file["Legal"] = Legal.to_json_users();
        json_file["ActiveDocuments"] = ActiveDocuments.to_json();
        json_file["ArchiveDocuments"] = ArchiveDocuments.to_json();

        return json_file;
    }

        void DocumentWorkflow::add_to_archive(Document archive_doc){
            ArchiveDocuments.add_document(archive_doc.to_json(),"ArchiveDocuments");
        }
        void DocumentWorkflow::add_to_storage(Document doc){
            ActiveDocuments.add_document(doc.to_json(),"ActiveStorage");
        }
    void DocumentWorkflow::add_user(User user){
        switch(user.get_ID()%10){
            case 1:
            administration.add_user(user);
            break;
            case 2:
            finances.add_user(user);
            break;
            case 3:
            HR.add_user(user);
            break;
            case 4:
            bookkeeping.add_user(user);
            break;
            case 5:
            Legal.add_user(user);
            break;
        }
    }
    void DocumentWorkflow::del_user(User user){
         switch(user.get_ID()%10){
            case 1:
            administration.del_user(user.get_ID());
            break;
            case 2:
            finances.del_user(user.get_ID());
            break;
            case 3:
            HR.del_user(user.get_ID());
            break;
            case 4:
            bookkeeping.del_user(user.get_ID());
            break;
            case 5:
            Legal.del_user(user.get_ID());
        }
    }

    void DocumentWorkflow::del_from_storage(int doc_id){
                ActiveDocuments.del_exact_doc("ActiveStorage",doc_id);
    }
        void DocumentWorkflow::del_from_archive(Document doc){
        ArchiveDocuments.del_doc(doc,"ArchiveDocuments");
    }
    void DocumentWorkflow::del_from_storage(Document doc){
                ActiveDocuments.del_doc(doc,"ActiveStorage");
    }
User DocumentWorkflow::find_user(int ID){
     switch(ID%10){
            case 1:
            return administration.find_user_by_ID(ID);
            break;
            case 2:
            return finances.find_user_by_ID(ID);
            break;
            case 3:
           return HR.find_user_by_ID(ID);
            break;
            case 4:
            return bookkeeping.find_user_by_ID(ID);
            break;
            case 5:
            return Legal.find_user_by_ID(ID);
        }
        return User();
}
    Storage& DocumentWorkflow::get_storage(){
        return ActiveDocuments;
    }

    void DocumentWorkflow::distribute_doc(int Department,EDocument doc,int amnt,User user){

        switch(Department){
             case 1:
            administration.distribute_doc(doc);
            break;
            case 2:
            finances.distribute_doc(doc);
            break;
            case 3:
            HR.distribute_doc(doc);
            break;
            case 4:
            bookkeeping.distribute_doc(doc);
            break;
            case 5:
            Legal.distribute_doc(doc);

        }
         switch(user.get_ID()%10){
             case 1:
            administration.del_doc(user,amnt);
            break;
            case 2:
            finances.del_doc(user,amnt);
            break;
            case 3:
            HR.del_doc(user,amnt);
            break;
            case 4:
            bookkeeping.del_doc(user,amnt);
            break;
            case 5:
            Legal.del_doc(user,amnt);
        }
    }
        Storage DocumentWorkflow::get_archive(){
            return ArchiveDocuments;
        }

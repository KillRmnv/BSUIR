#include "../src/Personal_account.h"
#include "../src/EDocument.h"
#include "../src/RevisionHistory.h"
#include "../src/SystemDate.h"
 EDocument Personal_account::create_doc(int user_ID,std::string type,std::string name,int id, std::string creation_date, std::string author,
 std::string expiry_date, SystemDate date,   std::string file_path){

 Comment creation_note("Created",user_ID,date.get_system_date());
 RevisionHistory history;history.add_new_log(date.get_system_date(),date.get_system_date(),creation_note);
 return EDocument(type,name,id,creation_date,author,expiry_date,false,false,history,file_path);
 }
    EDocument Personal_account::copy(){
            EDocument to_copy=current_doc;
            if(position->canCopy()){
        to_copy.change_to_copy_version();
        return to_copy;
        }
        return EDocument();
    }
    Employee* Personal_account::get_position(){
        return position;
    }
   void Personal_account::add_notifaction(Notification& new_one){
        receipts.push_back(new_one);
        return;
    }
 ActivityLog& Personal_account::get_log()  {
    return user_history;
    }
void Personal_account::updateToDoList(EDocument doc) {
    ToDoDocs.add_doc(doc);
    }
int Personal_account::amnt_of_docs() {
    return ToDoDocs.amnt_of_elements();
    }
DocsList& Personal_account::get_list() {
    return ToDoDocs;
    }
EDocument Personal_account::choose_from_list(int num) {
    EDocument eDoc;
    if (num < 0 || num >= ToDoDocs.amnt_of_elements()) {
        throw std::out_of_range("Invalid document index.");
    }
    EDocument doc=ToDoDocs.pop(num);

    return  eDoc;
   }

nlohmann::json Personal_account::to_json() const {
    nlohmann::json json_data;
    Employee pos(9,"hollow");
    json_data["ToDoDocs"] = ToDoDocs.to_json(); 
    json_data["user_history"] = user_history.to_json(); 
    json_data["current_doc"] = current_doc.to_json();
    nlohmann::json notes=nlohmann::json::array();
    for(auto note:receipts)
        notes.push_back(note.to_json());
    json_data["receipts"]=notes;
    if (position) {
    json_data["Employee"] = position->to_json();
} else {
    json_data["Employee"] = pos.to_json(); // Или другое значение по умолчанию
}

    return json_data;
}
Personal_account Personal_account::from_json(nlohmann::json json_file) {
    Personal_account account;std::string pos;int Dep;
    account.ToDoDocs = DocsList::from_json(json_file["ToDoDocs"]);
    account.user_history = ActivityLog::from_json(json_file["user_history"]);
    account.current_doc = EDocument::from_json(json_file["current_doc"]);
    nlohmann::json notes=nlohmann::json::array();
    notes=json_file["receipts"];
    nlohmann::json json_obj=json_file["Employee"];
    pos=json_obj["position"];
    Dep=json_obj["Department"];

    for(const auto& note:notes)
        account.receipts.push_back(Notification::from_json(note));
    
    return account;
}
    Personal_account::Personal_account(std::string Position_line){
        Identify_position(Position_line);
    }
    void Personal_account::Identify_position(std::string Position){
    if (Position == "Administrator")
        position=new Administrator;
    if (Position == "Bookkeeper")
        position=new Bookkeeper;
    if (Position == "FinManager")
        position=new FinManager;
    if (Position == "Lawyer")
        position=new Lawyer;
    }
    void Personal_account::set_doc(EDocument doc){
        current_doc=doc;
    }
     std::vector<Notification> Personal_account::get_notifications(){
        return receipts;
     }
   bool Personal_account::has_document(int id){
    return ToDoDocs.check_for_existance(id);
   }
#include "../src/DocsList.h"
EDocument& DocsList::pop(int index){
    return Documents[index-1];
}
void DocsList::DisplayList(){
    int counter=1;
    for(int i=0;i<Documents.size();i++){
        std::cout<<counter<<".";
        Documents[i].info_about_document();
    }
}
void DocsList::add_doc(EDocument new_doc){
    Documents.push_back(new_doc);
}   
    EDocument DocsList::mark_us_complete(int index){
    EDocument completed=Documents[index-1];
    Documents.erase(Documents.begin()+index-1);
    return completed;
}

nlohmann::json DocsList::to_json() const {
    nlohmann::json j;
    for ( Document doc : Documents) {
        j.push_back(doc.to_json());
    }
    return j;
}

 DocsList DocsList::from_json(nlohmann::json json_file) {
  DocsList DOCS;
    for ( auto item : json_file) {
        DOCS.add_doc(EDocument::from_json(item));
    }
    return DOCS;
}
    int DocsList::amnt_of_elements(){
        return Documents.size();
    }
        bool DocsList::check_for_existance(int id){
            for(size_t i=0;i<Documents.size();i++){
                if(Documents[i].get_ID()==id)
                return true;
            }
            return false;
        }

#include "../src/Storage.h"
 EDocument Storage::find_doc(int id){
    int choice,ID,counter=1;std::vector<int> indexes;
    indexes=indexByID[id];
    if(!indexes.empty())
    return EDocument::from_json(documents[indexes[0]]);
   return EDocument();
 }
 Storage& Storage::del_doc(Document doc,std::string storage_name){
    std::vector<int> indexes;
    indexes=indexByID[doc.get_ID()];
    documents.erase(documents.begin()+indexes[0]);
    storage_name+=".json";
    FileWriter storage_file;
    storage_file.rewrite(documents,storage_name);
    return *this;    
 }
Storage& Storage::del_exact_doc(std::string storage_name, int id) {
    for (auto it = documents.begin(); it != documents.end(); /* пусто */) {
        if (EDocument::from_json(*it).get_ID() == id) {
            it = documents.erase(it); // Удаляем элемент и обновляем итератор
        } else {
            ++it; // Переходим к следующему элементу
        }
    }

    storage_name += ".json";
    FileWriter storage_file;
    storage_file.rewrite(documents, storage_name);
    return *this;
}

Storage& Storage::add_document(nlohmann::json new_doc,std::string storage_name){
    documents.push_back(new_doc);
    std::vector<int> indexes;
    std::string param;
    param=new_doc.at("author").get<std::string>();
    indexByAuthor[param].push_back(documents.size()-1);
    param=new_doc.at("creation_date").get<std::string>();
    indexByDate[param].push_back(documents.size()-1);
    param=new_doc.at("type").get<std::string>();
    indexByType[param].push_back(documents.size()-1);
     int ID=new_doc.at("ID").get<int>();
    indexByID[ID].push_back(documents.size()-1);
    std:: string file_path="Json/"+storage_name;storage_name=file_path;
    storage_name+=".json";
    FileWriter storage_file;
    storage_file.rewrite(documents,storage_name);
    return *this;
}
 Storage::Storage(nlohmann::json docs_from_file){
    std::string param;int ID;
    for(int i=0;i<docs_from_file.size();i++){
    param=docs_from_file[i].at("author").get<std::string>();
    indexByAuthor[param].push_back(i);
    param=docs_from_file[i].at("creation_date").get<std::string>();
    indexByDate[param].push_back(i);
    param=docs_from_file[i].at("type").get<std::string>();
    indexByType[param].push_back(i);
    ID=docs_from_file[i].at("ID").get<int>();
    indexByID[ID].push_back(i);
    }
    documents=docs_from_file;
 }
 nlohmann::json Storage::to_json()
 {
   return documents;
 }
  bool Storage::check_for_existance(int id){
    std::vector<int> indexes=indexByID[id];
    if(indexes.empty())
        return false;
        return true;
  }
  bool Storage::is_empty(){
   return documents.empty();
  }
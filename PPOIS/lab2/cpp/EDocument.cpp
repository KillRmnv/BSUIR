#include "../src/EDocument.h"
        void EDocument::edit(int user_ID,std::string Name,std::string Type,std::string Creation_date,std::string Author,std::string Expiry_date){
            SystemDate date;Comment comment_to_editing("Editted",user_ID,date.get_system_date());
            name=Name;
            type=Type;
            creation_date=Creation_date;
            author=Author;
            expiry_date=Expiry_date;
            history.add_new_log(date.get_system_date(), date.get_system_date(), comment_to_editing);
        }
    
    void EDocument::DisplayComms(int num){
        
        for(int i=0;i<Comments_to_doc.size()&& i<num;i++){
            Comments_to_doc[i].DisplayText();
        }
    }

nlohmann::json EDocument::to_json()  const {

        nlohmann::json json_data = Document::to_json();
        json_data["path_to_file"] = path_to_file;
        json_data["Comments_to_doc"] = nlohmann::json::array();
        for (Comment comment : Comments_to_doc) {
            json_data["Comments_to_doc"].push_back(comment.to_json());
        }
        return json_data;
}
EDocument EDocument::from_json(nlohmann::json json_file){
    
       RevisionHistory History;
            if(json_file.contains("history"))
            History.from_json(json_file.at("history").get<nlohmann::json>());
        EDocument eDoc(
            json_file.at("type").get<std::string>(), 
            json_file.at("name").get<std::string>(),
            json_file.at("ID").get<int>(),
            json_file.at("creation_date").get<std::string>(),
            json_file.at("author").get<std::string>(),
            json_file.at("expiry_date").get<std::string>(),
            json_file.at("signature").get<bool>(),
            json_file.at("stamp").get<bool>(),
            History,
            json_file.at("path_to_file").get<std::string>()
        );
    if(json_file.contains("Comment_to_doc")){
    nlohmann::json comms=nlohmann::json::array();
    comms=json_file.at("Comment_to_doc").get<nlohmann::json>();
    
    for(int i=0;i<comms.size();i++)
        eDoc.Comments_to_doc.push_back(Comment::from_json(comms[i]));
    }
        return eDoc;
}
void EDocument::add_comment(Comment new_comment){
Comments_to_doc.push_back(new_comment);    
}
    void EDocument::open_in_text_editor(){
        std::string command;
          #if defined(_WIN32) || defined(_WIN64)
          command="rundll32.exe shell32.dll,OpenAs_RunDLL "+path_to_file;
          #elif defined(__linux__)
            command="mimeopen -d " + path_to_file;
            #endif
        std::system(command.c_str());
    }
       
    void EDocument::change_to_copy_version(){
        type[12]='2';
        name+= " copied";
    }
    void EDocument::aprove(){
        stamp=true;
    }
    void EDocument::sign(){
        signature=true;
    }
       std::vector<Comment> EDocument::get_comments(){
        return Comments_to_doc;
       }
        void EDocument::set_path_to_file(std::string path){
            path_to_file=path;
        }
        std::string EDocument::get_path_to_file(){
            return path_to_file;
        }

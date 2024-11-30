#include "../src/Comment.h"
nlohmann::json Comment::to_json() const {
        return nlohmann::json{
            {"text", text},
            {"user_ID", user_ID},
            {"date", date}
        };
    }
Comment Comment::from_json(const nlohmann::json & json_comment){
    Comment comment(
        json_comment.at("text").get<std::string>(),
        json_comment.at("user_ID").get<int>(),
        json_comment.at("date").get<std::string>() );
    return comment;
    }
void Comment::Edit(int editing_user_id,std::string Text){
        user_ID=editing_user_id;
        text=Text;
        SystemDate sysdate;
        date=sysdate.get_system_date();
}
int Comment::get_ID(){
    return user_ID; 
}
void Comment::DisplayText(){
    std::cout<<text<<std::endl<<user_ID<<std::endl<<date<<std::endl;
}
    std::string Comment::get_text(){
        return this->text;
    }
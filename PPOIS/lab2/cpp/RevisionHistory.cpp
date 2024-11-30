#include "../src/RevisionHistory.h"
    void RevisionHistory::Display(int num){
        for(long unsigned int i=0;i<num&&i<history.size();i++)
        history[i].Display();
    }

void RevisionHistory::from_json(nlohmann::json json_file){
    nlohmann::json historicalrecords=nlohmann::json::array();
    historicalrecords=json_file.at("history").get<nlohmann::json>();
    for(long unsigned int i=0;i<historicalrecords.size();i++){
    history.push_back(HistoricRecord::from_json(historicalrecords[i]));
    }
}  
void RevisionHistory::del_exact_log(  std::string DateArrival,std::string DateSend,int num){
    int counter=1;std::vector <int> indexes;
    for(int i=0;i<history.size();i++){
        if(DateArrival==history[i].get_date_arrival()&&DateSend==history[i].get_date_send()){
            std::cout<<counter<<".";
            history[i].get_comment().DisplayText();
            indexes.push_back(i);
        }
    }
    history.erase(history.begin()+indexes[num-1]);
}
nlohmann::json RevisionHistory::to_json() const {
    nlohmann::json History=nlohmann::json::array();
    if(history.empty()){
        return nullptr;
    }
    for(long unsigned int i=0;i<history.size();i++)
        History[i].push_back(history[i].to_json());
    return History;
}
RevisionHistory &RevisionHistory::add_new_log(std::string DateArrival, std::string DateSend,Comment note){
    history.push_back(HistoricRecord(DateArrival,DateSend,note));
    return *this;
}
    RevisionHistory&  RevisionHistory::del_logs(int amnt){
        for(int i=0;i<amnt;i++)
        history.erase(history.begin()+i);
        return *this;
    }
        Comment RevisionHistory::get_comment(int num){
            return history[num-1].get_comment();
        }
    std::vector<HistoricRecord> RevisionHistory::get_history() const{
        return history;
    }

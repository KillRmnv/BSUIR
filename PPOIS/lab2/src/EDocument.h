#pragma once

#include "Document.h"
#include "SystemDate.h"
class EDocument:public Document
{
    private:
    std::string path_to_file;
    std::vector<Comment> Comments_to_doc;

    public:
      ~EDocument() = default; 
    EDocument(std::string Type, std::string Name, int id, std::string Creation_date, std::string Author, 
              std::string Expiry_date, bool Signature, bool Stamp, RevisionHistory History, std::string Path_to_file)
        : Document(Type, Name, id, Creation_date, Author, Expiry_date, Signature, Stamp, History), 
          path_to_file(Path_to_file) {}        
        nlohmann::json to_json() const;
        static EDocument from_json(nlohmann::json json_file);
        using Document::from_json;
        using Document::Document;
        void add_comment(Comment new_comment);
        void open_in_text_editor();
        void change_to_copy_version();
        void edit(int user_ID,std::string Name,std::string Type,std::string Creation_date,std::string Author,std::string Expiry_date);
        EDocument(){}           
        void DisplayComms(int num);
          void aprove();
        void sign();
        std::vector<Comment> get_comments();
        void set_path_to_file(std::string path);
        std::string get_path_to_file();

};

    
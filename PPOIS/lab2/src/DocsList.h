#pragma once

#include "Document.h"
#include "EDocument.h"
#include<nlohmann/json.hpp>
class DocsList{
    private:
    std::vector<EDocument> Documents;
    public:
    void DisplayList();
    EDocument& pop(int index);
    void add_doc(EDocument new_doc);
     EDocument mark_us_complete(int index);
    nlohmann::json to_json() const;
    static DocsList from_json(nlohmann::json json_file);
    int amnt_of_elements();
    bool check_for_existance(int id);
};


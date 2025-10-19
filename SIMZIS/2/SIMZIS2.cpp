#include <algorithm>
#include <clocale>
#include <cstring>
#include <iostream>
#include <string>
#include <locale>
#include<vector>
#include<cmath>
using namespace std;
vector<vector<string>> create_table(string line_to_cypher,int len,int width){
    vector<vector<string>> tables;
    double l=line_to_cypher.size();
    std::string::iterator end_pos = std::remove(line_to_cypher.begin(), line_to_cypher.end(), ' ');
    line_to_cypher.erase(end_pos, line_to_cypher.end());
        for(int j=0;j<(line_to_cypher.length() + len * width - 1) / (len * width);j++){
        vector<string> table;
            for(int i=0;i<width;i++){
                if(line_to_cypher.length()<i*len+(width*len)*j+len){
                    if(i*len+(width*len)*j>=line_to_cypher.length()){
                        string newStr;
                        for(int t=0;t<len;t++){
                            newStr+=rand()%256;
                        }
                        table.push_back(newStr);
                    }
                    else{ 
                        table.push_back(line_to_cypher.substr(i*len+(width*len)*j));
                    while(table[table.size()-1].size()<len)
                        table[table.size()-1]+="*";
                    }
                }
                else
                    table.push_back(line_to_cypher.substr(i*len+(width*len)*j,len));
            }
        tables.push_back(table);
    }
    return tables;
}

void output(vector<vector<string>> tables){
    for(auto table:tables){
        for(auto line:table){
            cout<<line<<endl;
        }
    }
}
string to_encrypt(vector<vector<string>> tables,int len){
    
    string result;
    for(int pos=0;pos<len;pos++){
        for(auto table:tables){
            for(auto line:table){
                result+=line[pos];
            }
        }
    }
    return result;
}
void to_decrypt(string secret_line){
    int len=1,width=1;
    for(;len<secret_line.length();len++){
        for(width=1;width*len<secret_line.length();width++);
        if(width*len!=secret_line.length()){
            continue;
        }else{
            vector<string>table;
            for(int start=0;start<secret_line.length();start+=len){
                table.push_back(secret_line.substr(start,len));
            }
            string line;
            for(int pos=0;pos<len;pos++){
                for(auto tline:table){
                    line+=tline[pos];
                }
            }
            cout<<line<<endl;
        }
        
    }
}
int main(){
    setlocale(LC_ALL, "");
    string line_to_cypher;
    cout<<"Фраза:";
    getline(cin,line_to_cypher);
    cout<<"Длина таблицы:";
    int len,width;
    cin>>len;
    cout<<"Ширина таблицы:";
    cin>>width;
    vector<vector<string>> tables=create_table( line_to_cypher,  len,  width);
    output( tables);
    string secret_line=to_encrypt(tables,  len);
    cout<<"Зашифрованно:"<<secret_line<<endl<<"Возможные варианты:";
    to_decrypt( secret_line);
}
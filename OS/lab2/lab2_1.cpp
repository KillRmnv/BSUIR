#include <sys/types.h>
#include <unistd.h>
#include <string>
#include <iostream>
#include<vector>
#include <cstdlib>
#include <sys/wait.h> 
using namespace std;
void waiting(){
    do{
        waitpid(-1, nullptr, WNOHANG | WUNTRACED);
    }while(waitpid(-1, nullptr, WNOHANG | WUNTRACED)!=-1);
}
vector<int> parse(std::string line){
int ind=0,counter=0;vector<int> tree;
    while(line[ind]!='\0'){
        for(;line[ind]==' '&&line[ind]!='\0';ind++);
        for(counter=ind;line[counter]!=' '&&line[counter]!='\0';counter++);
        if(counter!=ind)
            tree.push_back(stoi(line.substr(ind,counter-ind)));
        ind=counter;
    }
return tree;
}
int main()
{
   std::string input;
   std::cout<<"Enter line:";
   getline(std::cin,input);
   vector<int> tree=parse(input);



   pid_t* tree_of_flow=new pid_t[tree.size()];
   pid_t buff;int num=1;
   for(size_t i=1;i<tree.size();++i){
    tree_of_flow[i]=0;
    }
    tree_of_flow[0]=getpid();
    buff=fork();
     if(buff==0){
    num=2;
    tree_of_flow[1]=getpid();
    }else
        if(buff<0){
        std::cout<<"ERROR";
        return 1;
    }


   for(size_t i=2;i<tree.size();++i){
    if(getpid()==tree_of_flow[tree[i]-1]){
    buff=fork();
     
    if(buff<0){
        std::cout<<"ERROR";
        return 1;
    }
    if(buff==0){
    num=i+1;
    tree_of_flow[i]=getpid();
     }


    }
   }
    waiting();
    while(true){
        std::cout<<"Process number:"<<num<<endl;
        std::cout<<"pid:"<<getpid()<<endl;               
        std::cout<<"ppid:"<<getppid()<<endl;
        std::cout<<"Current time:"<<200*num<<endl;
        usleep(1000 * 200*num);
    }
}

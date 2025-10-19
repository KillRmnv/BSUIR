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
    std::cout<<"PID:"<<getpid()<<" PPID:"<<getppid()<<endl;
   std::string input;
   std::cout<<"Enter line:";
   getline(std::cin,input);
   vector<int> tree=parse(input);
   std::cout<<"Enter path:";
   std::getline(std::cin,input);
   if(chdir(input.c_str())!=0){
        std::cout<<"ERROR OCCURED WHILE CHANGING DIR"<<endl;
    }
   pid_t* tree_of_flow=new pid_t[tree.size()];
   pid_t buff;int num=1;
   for(size_t i=1;i<tree.size();++i)
    tree_of_flow[i]=0;
    tree_of_flow[0]=getpid();
    buff=fork();
     if(buff==0){
    num=2;
    tree_of_flow[1]=getpid();
    std::cout<<"PROCESS ID:"<<getppid()<<" GIVE BIRTH TO PROCESS ID:"<<getpid()<<endl;
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
    std::cout<<"PROCESS ID:"<<getppid()<<" GIVE BIRTH TO PROCESS ID:"<<getpid()<<endl;
     }
    }
   }
    waiting();
    std::cout<<"Process number:"<<num<<endl;
    std::cout<<"pid:"<<getpid()<<endl;
    std::cout<<"ppid:"<<getppid()<<endl;
    if(num==6){
        usleep(1000 * 1000);
        std::cout<<endl<<"PID:"<<getpid()<<" PPID:"<<getppid()<<endl;
        execl("/bin/ls","ls","-l",nullptr);
    }
    waiting();
    std::cout<<"Process with PID:"<<getpid()<<" and PPID:"<<getppid()<<" ARE GONE"<<endl;
    exit(0);
}
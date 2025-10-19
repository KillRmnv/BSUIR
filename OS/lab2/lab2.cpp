#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <chrono>
#include <sys/wait.h> 
#include <ctime>
#include <iomanip>
using namespace std;
void waiting(){
    do{
        waitpid(-1, nullptr, WNOHANG | WUNTRACED);
    }while(waitpid(-1, nullptr, WNOHANG | WUNTRACED)!=-1);
}
int main(){
    pid_t process=getpid();
    pid_t buff;
    buff=fork();
    if(buff>0){
        buff=fork();
    }
    if(buff<0){
        std::cout<<"ERROR";
        return 1;
    }
   std::time_t now = std::time(nullptr);
    std::tm* localTime = std::localtime(&now);
    std::cout <<"PID:"<<getpid()<<" PPID:"<<getppid()<<" TIME:"<< std::put_time(localTime, "%H:%M:%S") << std::endl;
    waiting();
    if(getpid()==process)
        execl("/bin/ps","ps","-x",nullptr);
    exit(0);
}
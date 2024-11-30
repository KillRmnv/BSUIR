#include"../Headers/Person.h"
    Person::Person(std::string Name,std::string SecondName,int Age){
        name=Name;secondName=SecondName;age=Age;
    }
    std::string Person::sayName(){
        return name;
    }
    std::string Person::saySecondName(){
        return secondName;
    }
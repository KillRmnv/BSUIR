#pragma once
#include<string>

class Person{
    protected:
    std::string name;
    std::string secondName;
    int age;
    public:
    std::string sayName();
    std::string saySecondName();
    Person()=default;
    Person(std::string Name,std::string SecondName,int Age);
};
package by.romanov.ppois.InvestigationDepartment;


import by.romanov.ppois.ConsoleInput;
import by.romanov.ppois.Input;

public class InvestigationDepartmentInput {
    Input input;
    public InvestigationDepartmentInput(Input input) {
        this.input = input;
    }
    public InvestigationDepartmentInput(){
        input=new ConsoleInput();
    }
    public int chooseCase(int size){
        return input.getChoice("Выберите дело:",0,size-1);
    }
//    public void interview(String witnesse, Traits traits){
//        input.show(witnesse);
//
//        input.show("Цвет волос: "+traits.getHairColor());
//        input.showNumericRange("Вес: ",traits.getWeight()/1000,traits.getWeight()%1000);
//        input.showNumericRange("Рост: ",traits.getHeight()/1000,traits.getHeight()%1000);
//        input.showNumericRange("Возраст: ",traits.getAge()/100,traits.getAge()%100);
//    }
//    public void noCaseMessage(){
//        input.show("Нет дел");
//    }



}

package by.romanov.ppois.HRDepartment;

import by.romanov.ppois.Input;

import java.util.List;

public class HRDepartmentInput {
    Input input;

    public HRDepartmentInput(Input input) {
        this.input = input;
    }

    public HRDepartmentInput() {
    }
    public int chooseOption(){
        return input.getChoice("""
                1. Нанять
                2. Уволить
                """,1,2);
    }
    public void showPoliceManInfo(List<String> messages,int num) {
        input.showNum(num);
        input.show(messages);
    }
    public int getPoliceManHireChoice() {
        return input.getChoice("Выберите полицеского для найма:",0,11);
    }
    public int getPoliceManFireChoice(int size){
        return input.getChoice("Выберите полицеского для увольнения:",0,size);
    }
    public void showLastTwoHireOptions() {
        input.show("""
                10.Обновить
                11.Назад
                """);
    }
    public void showLastFireOption(int size){
        input.show(size+".  Назад");
    }
    public void showBudget(int budget) {
        input.show("Бюджет:"+budget);
    }


}

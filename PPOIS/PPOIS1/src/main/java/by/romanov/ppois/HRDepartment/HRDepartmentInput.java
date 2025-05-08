package by.romanov.ppois.HRDepartment;

import by.romanov.ppois.Input;
import by.romanov.ppois.UserInterface;

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
    public int getPoliceManHireChoice() {
        return input.getChoice("Выберите полицеского для найма:",0,11);
    }
    public int getPoliceManFireChoice(int size){
        return input.getChoice("Выберите полицеского для увольнения:",0,size);
    }




}

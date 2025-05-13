package by.romanov.ppois.StateMachine.InvestigationDepartment;


import by.romanov.ppois.Ui.ConsoleInput;


public class InvestigationDepartmentInput {
    ConsoleInput input;
    public InvestigationDepartmentInput(ConsoleInput input) {
        this.input = input;
    }
    public InvestigationDepartmentInput(){
        input=new ConsoleInput();
    }
    public int chooseCase(int size)  {
        return input.getChoice("Выберите дело:",0,size-1);
    }


}

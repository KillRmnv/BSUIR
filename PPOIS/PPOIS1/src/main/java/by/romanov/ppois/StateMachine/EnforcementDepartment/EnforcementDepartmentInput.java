package by.romanov.ppois.StateMachine.EnforcementDepartment;



import by.romanov.ppois.Ui.ConsoleInput;

import java.util.Map;

public class EnforcementDepartmentInput {
    private ConsoleInput input;
    public EnforcementDepartmentInput(){

    }
    public EnforcementDepartmentInput(ConsoleInput input) {
        this.input = input;
    }
    public int chooseCase(int size)    {
        return input.getChoice("Выберите дело:", 0, size - 1);
    }
    public <K,V>  int choosePoliceMan(Map<K,V> map)    {
       return  input.getChoiceFromMap("",map);
    }
    public int chooseAction()    {
        return input.getChoice("""
                1.QuickTimeEvent
                2.Бросок кубика
                """,1,2);
    }
    public int askForRepeat()    {
        return input.getChoice("""
                1.Попробовать снова
                2.Упустить преступника
                """,1,2);
    }

}

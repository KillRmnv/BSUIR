package by.romanov.ppois.EnforcementDepartment;

import by.romanov.ppois.Input;

import java.lang.reflect.InvocationTargetException;
import java.util.Map;

public class EnforcementDepartmentInput {
    private Input input;
    public EnforcementDepartmentInput(){

    }
    public EnforcementDepartmentInput(Input input) {
        this.input = input;
    }
    public int chooseCase(int size) {
        return input.getChoice("Выберите дело:", 0, size - 1);
    }
    public <K,V>  int choosePoliceMan(Map<K,V> map) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
       return  input.getChoiceFromMap("Выберите полицейского:",map);
    }
    public int chooseAction(){
        return input.getChoice("""
                1.QuickTimeEvent
                2.Бросок кубика
                """,1,2);
    }
    public int askForRepeat(){
        return input.getChoice("""
                1.Попробовать снова
                2.Упустить преступника
                """,1,2);
    }

}

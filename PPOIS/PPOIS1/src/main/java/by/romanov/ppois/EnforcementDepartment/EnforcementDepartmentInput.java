package by.romanov.ppois.EnforcementDepartment;

import by.romanov.ppois.Input;
import by.romanov.ppois.Law;

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
    public void Failure(){
        input.show("Преступник ускользнул!");
    }
    public void Success(){
        input.show("Преступник пойман!");
    }
    public void suspectCaught(Law law){
        input.show("""
                Преступник пойман и наказан:
                """+law.getPunishment());
    }
    public void deathOfPoliceman(){
        input.show("Критический провал:полицейский убит,преступник ускользнул!");
    }
    public void qteMessage(){
        input.show("Быстро нажмите ПРОБЕЛ (у вас 2 секунды)!");
    }
    public void qteMessageCriticFailure(){
        input.show("Критическая ситуация:быстро нажмите ПРОБЕЛ (у вас 2 секунды)!");
    }
    public void suspectEscaped(){
        input.show("Преступник скрылся. Дело отправлено в архив");
    }
    public void noCaseMessage(){
        input.show("Дел нет");
    }
    public void successQTE(){
        input.show("Шанс поимки увеличен!");
    }
    public void failureQTE(){
        input.show("Вы не успели");
    }
}

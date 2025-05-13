package by.romanov.ppois.StateMachine.PublicSafetyDepartment;


import by.romanov.ppois.Ui.ConsoleInput;

import java.util.List;

public class PublicSafetyDepartmentInput  {
    ConsoleInput input;
    public PublicSafetyDepartmentInput(ConsoleInput input) {
        this.input = input;
    }
    public PublicSafetyDepartmentInput(){}
    public int chooseOption()   {
       return input.getChoice("""
                1.Отправить агитировать в школу
                2.Патрулировать районы
                """,1,2);
    }
    public int chooseSchool()   {
        return input.getChoice("""
                Номер школы:
                """,1,99);
    }
    public int chooseCityArea( List<String> areas)   {
        return input.getChoice(areas,0,areas.size()-1);
    }

}

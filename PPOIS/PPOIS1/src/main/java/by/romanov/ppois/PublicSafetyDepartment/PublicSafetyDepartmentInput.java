package by.romanov.ppois.PublicSafetyDepartment;

import by.romanov.ppois.Input;
import java.util.List;

public class PublicSafetyDepartmentInput  {
    Input input;
    public PublicSafetyDepartmentInput(Input input) {
        this.input = input;
    }
    public PublicSafetyDepartmentInput(){}
    public int chooseOption(){
       return input.getChoice("""
                1.Отправить агитировать в школу
                2.Патрулировать районы
                """,1,2);
    }
    public int chooseSchool(){
        return input.getChoice("""
                Номер школы:
                """,1,99);
    }
    public int chooseCityArea( List<String> areas){
        return input.getChoice(areas,0,areas.size()-1);
    }
    public void showPatrolingArea(String area){
        input.show("Патруль отправился в "+area+" район");
    }
    public void showSchool(String school){
        input.show("Патруль отправился в "+school);
    }
    public void newCaseMessage(){
        input.show("""
                    На улицах произошло преступление,загляните в отдел расследований
                """);
    }
}

package by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentsStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentInput;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.*;

public class HirePoliceManState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        HRDepartmentContext hrContext = (HRDepartmentContext) context;
        HRDepartmentInput input=new HRDepartmentInput( hrContext.getInput());
        Map<Integer,PoliceMan> newPoliceMans =null;
        int choice = 0;
        context.getUserInterface().show("Бюджет:" + hrContext.getBudget());
        do {
            newPoliceMans=hrContext.getHrService().generateNewPoliceMans();
            context.getUserInterface().showMap(newPoliceMans,"Выберите полицеского для найма:");
            context.getUserInterface().show("""
                10. Обновить
                11. Назад
                """);

           choice=  input.getPoliceManHireChoice();
            if (choice == 11) {
                break;
            }else if (choice !=10) {
               try {
                   hrContext.addPoliceMan(newPoliceMans.get(choice));
               }catch (Exception e){
                   System.out.println(e.getMessage());
                   choice=10;
               }
            }
            newPoliceMans.clear();
        }
        while (choice==10) ;
    }

    @Override
    public State next(Context context) {
        return null;
    }
}

package by.romanov.ppois.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Context;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.Police.PoliceStates.NewCaseState;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.State;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class AreasPatrolState implements State {
    @Override
    public void run(Context context) {
        PublicSafetyDepartmentInput pubSafeInput=new PublicSafetyDepartmentInput( context.getInput());
        List<String> areas = new ArrayList<>(Arrays.asList("Советский", "Центральный", "Первомайский", "Партизанский", "Заводской",
                "Ленинский", "Октябрьский", "Московский", "Фрунзенский"));
        int choice=pubSafeInput.chooseCityArea(areas);
        context.getUserInterface().show("Патруль отправился в "+areas.get(choice)+" район");
    }

    @Override
    public State next(Context context) {
        PublicSafetyDepartmentContext pubSafeContext = (PublicSafetyDepartmentContext) context;
        PublicSafetyDepartmentInput pubSafeInput=new PublicSafetyDepartmentInput( context.getInput());
        Random crime=new Random();
        if(crime.nextInt(100)<60){
            context.getUserInterface().show("На улицах произошло преступление,загляните в отдел расследований");
            pubSafeContext.setNext(new NewCaseState());
            pubSafeContext.getTransfer().setCaseData(new Case(pubSafeContext.getCriminalLaws()));
        }else{
            pubSafeContext.setNext(new InitialState());
        }

        return null;
    }
}

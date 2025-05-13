package by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentsStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentInput;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;

public class FirePoliceManState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        HRDepartmentContext hrContext = (HRDepartmentContext) context;
        HRDepartmentInput input = new HRDepartmentInput( hrContext.getInput());
        List<PoliceMan> policeManList = new ArrayList<>(hrContext.getHrService().getPoliceManRepository().loadAll().values());
        context.getUserInterface().show("Бюджет:"+hrContext.getBudget());
        context.getUserInterface().showMap(hrContext.getHrService().getPoliceManRepository().loadAll(),"Выберите полицейского:");
        context.getUserInterface().show(policeManList.size()+". Назад");
        int choice =  input.getPoliceManFireChoice(policeManList.size());
        if (choice != policeManList.size()) {
            hrContext.delPoliceMan(choice);
            context.getUserInterface().show("Бюджет:" + hrContext.getBudget());
        }
    }

    @Override
    public State next(Context context) {
        return null;
    }
}

package by.romanov.ppois.HRDepartment.HRDepartmentsStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartmentInput;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.State;

import java.util.ArrayList;
import java.util.List;

public class FirePoliceManState implements State {
    @Override
    public void run(Context context) {
        HRDepartmentContext hrContext = (HRDepartmentContext) context;
        HRDepartmentInput input = new HRDepartmentInput( hrContext.getInput());
        List<PoliceMan> policeManList = new ArrayList<>(hrContext.getPoliceMans().values());
        context.getUserInterface().show("Бюджет:"+hrContext.getBudget());

        for (int index = 0; index < policeManList.size(); index++) {
            context.getUserInterface().showNum(index);
            context.getUserInterface().show(policeManList.get(index).Info());
        }
        context.getUserInterface().show(policeManList.size()+". Назад");
        int choice = input.getPoliceManFireChoice(policeManList.size());
        if (choice != policeManList.size()) {
            hrContext.delPoliceMan(policeManList.get(choice).getId());
            context.getUserInterface().show("Бюджет:" + hrContext.getBudget());
        }
    }

    @Override
    public State next(Context context) {
        return null;
    }
}

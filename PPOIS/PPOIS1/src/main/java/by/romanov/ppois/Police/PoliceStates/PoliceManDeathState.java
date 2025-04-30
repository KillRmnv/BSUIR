package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.State;
import by.romanov.ppois.StateMachine;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

public class PoliceManDeathState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        PoliceContext policeContext = (PoliceContext) context;
        int policeMan = ((EnforcementDepartmentContext) policeContext.getEnforcementDepartment().getContext()).getPoliceMan();
        ((HRDepartmentContext) policeContext.getHrDepartment().getContext()).delPoliceMan(policeMan);
        StateMachine.saveContextToFile(policeContext.getHrDepartment().getContext());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new InitialState();
    }
}

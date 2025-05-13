package by.romanov.ppois.StateMachine.Police.PoliceStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentStates.ChooseCaseState;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.State;


import java.lang.reflect.InvocationTargetException;


public class InvestigationDepartmentState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext contextPolice = (PoliceContext) context;
        contextPolice.getInvestigationDepartment().runAll(new ChooseCaseState());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        PoliceContext contextPolice = (PoliceContext) context;
        return contextPolice.getInvestigationDepartment().getContext().getNextState();

    }
}

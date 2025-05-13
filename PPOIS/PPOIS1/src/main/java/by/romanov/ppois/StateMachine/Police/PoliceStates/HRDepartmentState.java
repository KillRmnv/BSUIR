package by.romanov.ppois.StateMachine.Police.PoliceStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentsStates.InitialState;
import by.romanov.ppois.StateMachine.State;


import java.lang.reflect.InvocationTargetException;



public class HRDepartmentState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext contextPolice = (PoliceContext) context;
        contextPolice.getHrDepartment().runAll(new InitialState());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        PoliceContext contextPolice = (PoliceContext) context;
        return contextPolice.getHrDepartment().getContext().getNextState();
    }
}

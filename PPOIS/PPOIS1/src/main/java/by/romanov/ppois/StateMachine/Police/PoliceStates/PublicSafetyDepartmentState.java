package by.romanov.ppois.StateMachine.Police.PoliceStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyStates.InitialState;
import by.romanov.ppois.StateMachine.State;
import java.lang.reflect.InvocationTargetException;

public class PublicSafetyDepartmentState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext contextPolice = (PoliceContext) context;
        contextPolice.getPublicSafetyDepartment().runAll(new InitialState());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        PoliceContext contextPolice = (PoliceContext) context;
        return  contextPolice.getPublicSafetyDepartment().getContext().getNextState();
    }
}

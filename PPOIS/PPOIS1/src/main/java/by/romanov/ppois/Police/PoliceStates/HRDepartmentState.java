package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.State;


import java.lang.reflect.InvocationTargetException;



public class HRDepartmentState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext contextPolice = (PoliceContext) context;
        contextPolice.getHrDepartment().runAll(new by.romanov.ppois.HRDepartment.HRDepartmentsStates.InitialState());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        PoliceContext contextPolice = (PoliceContext) context;
        return contextPolice.getHrDepartment().getContext().getNextState();
    }
}

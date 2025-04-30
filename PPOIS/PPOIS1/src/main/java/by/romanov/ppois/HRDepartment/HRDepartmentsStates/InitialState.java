package by.romanov.ppois.HRDepartment.HRDepartmentsStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartmentInput;
import by.romanov.ppois.State;

public class InitialState implements State {
    @Override
    public void run(Context context) {

    }

    @Override
    public State next(Context context) {

        HRDepartmentContext hrContext = (HRDepartmentContext) context;

        HRDepartmentInput input=new HRDepartmentInput( hrContext.getInput());
        switch (input.chooseOption()){
            case 1->{
                return new HirePoliceManState();
            }
            case 2->{
                return new FirePoliceManState();
            }
        }
        return null;
    }
}

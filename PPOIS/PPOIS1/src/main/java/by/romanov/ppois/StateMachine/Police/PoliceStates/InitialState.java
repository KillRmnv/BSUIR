package by.romanov.ppois.StateMachine.Police.PoliceStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Department;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.Police.PoliceInput;
import by.romanov.ppois.StateMachine.State;

import java.lang.reflect.InvocationTargetException;

public class InitialState implements State {
    @Override
    public void run(Context context) {
        PoliceContext policeContext = (PoliceContext) context;
        PoliceInput policeInput = new PoliceInput(policeContext.getInput());
        Department department = Department.fromCode(policeInput.chooseDepartment());
        policeContext.setDepartment(department);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        PoliceContext contextPolice = (PoliceContext) context;
        return switch (contextPolice.getChoice()) {
            case CONTROL_CENTRE -> new ControleCentreState();
            case INVESTIGATION_DEPARTMENT -> new InvestigationDepartmentState();
            case ENFORCEMENT_DEPARTMENT -> new EnforcementDepartmentState();
            case HR_DEPARTMENT -> new HRDepartmentState();
            case PUBLIC_SAFETY_DEPARTMENT -> new PublicSafetyDepartmentState();
            case POLICE -> new InitialState();
            default -> null;
        };
    }
}
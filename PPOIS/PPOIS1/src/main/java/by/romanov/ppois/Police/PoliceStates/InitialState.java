package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.Department;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.Police.PoliceInput;
import by.romanov.ppois.State;

import java.lang.reflect.InvocationTargetException;

public class InitialState implements State {
    @Override
    public void run(Context context) {
        PoliceContext policeContext = (PoliceContext) context;
        PoliceInput policeInput = new PoliceInput(policeContext.getInput());
        int choiceCode = policeInput.chooseDepartment();
        Department department = Department.fromCode(choiceCode);
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
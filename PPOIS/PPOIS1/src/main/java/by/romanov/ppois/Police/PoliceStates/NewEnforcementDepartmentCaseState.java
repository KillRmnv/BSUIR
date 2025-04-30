package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;

import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.State;
import by.romanov.ppois.StateMachine;


import java.lang.reflect.InvocationTargetException;



public class NewEnforcementDepartmentCaseState implements State {

    @Override
    public void run(Context context) throws Exception {
        PoliceContext policeContext = (PoliceContext) context;
        var newCase = ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).getTransfer().getCaseData();
        ((EnforcementDepartmentContext) policeContext.getEnforcementDepartment().getContext()).addCase(newCase);
        StateMachine.saveContextToFile(policeContext.getInvestigationDepartment().getContext());
        StateMachine.saveContextToFile(policeContext.getEnforcementDepartment().getContext());
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new InitialState();
    }
}

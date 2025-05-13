package by.romanov.ppois.StateMachine.Police.PoliceStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.State;

import java.lang.reflect.InvocationTargetException;


public class NewCaseState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext policeContext = (PoliceContext) context;

        Case newCase = policeContext.getControlCentre().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getControlCentre().getContext().getTransfer().setCaseData(null);
        }
        
        newCase = policeContext.getPublicSafetyDepartment().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getPublicSafetyDepartment().getContext().getTransfer().setCaseData(null);
        }

    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new InitialState();
    }
}

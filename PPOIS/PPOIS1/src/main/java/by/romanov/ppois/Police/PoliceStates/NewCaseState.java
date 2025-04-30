package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.Case;
import by.romanov.ppois.Context;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.State;
import by.romanov.ppois.StateMachine;

import java.lang.reflect.InvocationTargetException;


public class NewCaseState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext policeContext = (PoliceContext) context;

        Case newCase = policeContext.getControlCentre().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getControlCentre().getContext().getTransfer().setCaseData(null);
            StateMachine.saveContextToFile(policeContext.getControlCentre().getContext());
            StateMachine.saveContextToFile(policeContext.getInvestigationDepartment().getContext());
        }
        newCase = policeContext.getPublicSafetyDepartment().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getPublicSafetyDepartment().getContext().getTransfer().setCaseData(null);
            StateMachine.saveContextToFile(policeContext.getPublicSafetyDepartment().getContext());
            StateMachine.saveContextToFile(policeContext.getInvestigationDepartment().getContext());
        }

    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new InitialState();
    }
}

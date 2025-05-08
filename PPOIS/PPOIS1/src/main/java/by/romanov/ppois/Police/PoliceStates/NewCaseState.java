package by.romanov.ppois.Police.PoliceStates;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.Police.PoliceContext;

import java.lang.reflect.InvocationTargetException;


public class NewCaseState implements State {
    @Override
    public void run(Context context) throws Exception {
        PoliceContext policeContext = (PoliceContext) context;

        Case newCase = policeContext.getControlCentre().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getControlCentre().getContext().getTransfer().setCaseData(null);
            context.getSource().saveContextToFile(policeContext.getControlCentre().getContext());
            context.getSource().saveContextToFile(policeContext.getInvestigationDepartment().getContext());
        }
        
        newCase = policeContext.getPublicSafetyDepartment().getContext().getTransfer().getCaseData();
        if (newCase!=null&&!newCase.empty()) {
            ((InvestigationDepartmentContext) policeContext.getInvestigationDepartment().getContext()).addCase(newCase);
            policeContext.getPublicSafetyDepartment().getContext().getTransfer().setCaseData(null);
            context.getSource().saveContextToFile(policeContext.getPublicSafetyDepartment().getContext());
            context.getSource().saveContextToFile(policeContext.getInvestigationDepartment().getContext());
        }

    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new InitialState();
    }
}

package by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;

public class InitialState implements State {
    @Override
    public void run(Context context) throws IOException {
        EnforcementDepartmentContext enforcementDepartmentContext = (EnforcementDepartmentContext) context;
        EnforcementDepartmentInput input = new EnforcementDepartmentInput(enforcementDepartmentContext.getInput());
        var cases=enforcementDepartmentContext.findActiveCases();
        context.getTransfer().setCaseData(null);
        if (!cases.isEmpty()) {
            if(enforcementDepartmentContext.getPoliceManRepository().loadAll().isEmpty()) {
                context.getUserInterface().show("Полицейских нет");
                enforcementDepartmentContext.setNextStage(new InitialState());
                return;
            }else {
                enforcementDepartmentContext.getTransfer().setCaseData(cases.get(input.
                        chooseCase(cases.size())));
            }
        } else {
            context.getUserInterface().show("Дел нет");
            enforcementDepartmentContext.setNextStage(new InitialState());
        }
    }

    @Override
    public State next(Context context) throws IOException {
        if(context.getTransfer().getCaseData() == null) {
            return null;
        }
        return new CatchingSuspectState();
    }
}

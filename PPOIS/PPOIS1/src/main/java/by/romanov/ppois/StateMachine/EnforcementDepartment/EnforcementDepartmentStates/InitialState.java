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
        if (!cases.isEmpty()) {
            enforcementDepartmentContext.getTransfer().setCaseData(cases.get(input.
                    chooseCase(cases.size())));
        } else {
            context.getUserInterface().show("Дел нет");
            enforcementDepartmentContext.setNextStage(new InitialState());
        }
    }

    @Override
    public State next(Context context) throws IOException {
        if(((EnforcementDepartmentContext) context).findActiveCases().isEmpty()) {
            return null;
        }
        return new CatchingSuspectState();
    }
}

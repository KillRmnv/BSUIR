package by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.State;

public class InitialState implements State {
    @Override
    public void run(Context context) {
        EnforcementDepartmentContext enforcementDepartmentContext = (EnforcementDepartmentContext) context;
        EnforcementDepartmentInput input = new EnforcementDepartmentInput(enforcementDepartmentContext.getInput());
        if (!enforcementDepartmentContext.getCases().isEmpty()) {
            enforcementDepartmentContext.setChoice(input.
                    chooseCase(enforcementDepartmentContext.getCases().size()));
        } else {
            context.getUserInterface().show("Дел нет");
            enforcementDepartmentContext.setNextStage(new InitialState());
        }
    }

    @Override
    public State next(Context context) {
        if(((EnforcementDepartmentContext) context).getCases().isEmpty()) {
            return null;
        }
        return new CatchingSuspectState();
    }
}

package by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.Department;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentInput;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.State;

public class ChooseCaseState implements State {

    @Override
    public void run(Context context) {
        InvestigationDepartmentContext investigationDepartmentContext = (InvestigationDepartmentContext) context;
        InvestigationDepartmentInput input = new InvestigationDepartmentInput(investigationDepartmentContext.getInput());
        if (!investigationDepartmentContext.getCases().isEmpty()) {
            investigationDepartmentContext.setCurrentCase(investigationDepartmentContext.getCases().
                    get(input.chooseCase(investigationDepartmentContext.getCases().size())));
        } else {
            context.getUserInterface().show("Дел нет");
        }
    }

    @Override
    public State next(Context context) {
        if (!((InvestigationDepartmentContext) context).getCases().isEmpty())
            return new InterviewingWitnessesState();
        ((InvestigationDepartmentContext) context).setChoice(new InitialState());
        return null;
    }
}

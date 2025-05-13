package by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentInput;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;

public class ChooseCaseState implements State {

    @Override
    public void run(Context context) throws IOException {
        InvestigationDepartmentContext investigationDepartmentContext = (InvestigationDepartmentContext) context;
        InvestigationDepartmentInput input = new InvestigationDepartmentInput(investigationDepartmentContext.getInput());
        var cases=investigationDepartmentContext.findActiveCases();
        investigationDepartmentContext.getTransfer().setCaseData(null);
        if (!cases.isEmpty()) {
            int choice=input.chooseCase(cases.size());
            investigationDepartmentContext.getTransfer().setCaseData(cases.get(choice));
            investigationDepartmentContext.getTransfer().setChoice(choice);
        } else {
            context.getUserInterface().show("Дел нет");
        }
    }

    @Override
    public State next(Context context) throws IOException {
        if ( context.getTransfer().getCaseData() != null)
            return new InterviewingWitnessesState();
        ((InvestigationDepartmentContext) context).setChoice(new InitialState());
        return null;
    }
}

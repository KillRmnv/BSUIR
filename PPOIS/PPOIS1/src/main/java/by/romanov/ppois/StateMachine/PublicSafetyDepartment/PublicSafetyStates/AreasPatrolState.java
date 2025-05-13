package by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.Police.PoliceStates.NewCaseState;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class AreasPatrolState implements State {
    @Override
    public void run(Context context) {
        PublicSafetyDepartmentInput pubSafeInput = new PublicSafetyDepartmentInput(context.getInput());
        PublicSafetyDepartmentContext pubSafeContext = (PublicSafetyDepartmentContext) context;
        List<String> areas =pubSafeContext.getPublicSafetyService().getAreas();
        context.getUserInterface().show("Патруль отправился в " + areas.get(pubSafeInput.chooseCityArea(areas)) + " район");
    }

    @Override
    public State next(Context context) throws IOException {
        PublicSafetyDepartmentContext pubSafeContext = (PublicSafetyDepartmentContext) context;
        pubSafeContext.getTransfer().setCaseData(pubSafeContext.getPublicSafetyService().checkForCrime());
        if (pubSafeContext.getTransfer().getCaseData() == null) {
            pubSafeContext.setNext(new InitialState());
        } else {
            context.getUserInterface().show("На улицах произошло преступление,загляните в отдел расследований");
            pubSafeContext.setNext(new NewCaseState());
        }
        return null;
    }
}

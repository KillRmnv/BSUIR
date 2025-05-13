package by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.StateMachine.State;

public class SchoolCampaigningState implements State {
    @Override
    public void run(Context context) {
        PublicSafetyDepartmentContext publicSafetyDepartmentContext = (PublicSafetyDepartmentContext) context;
        PublicSafetyDepartmentInput pubSafeInput=new PublicSafetyDepartmentInput(publicSafetyDepartmentContext.getInput());

        String school="Школа №"+pubSafeInput.chooseSchool();
        context.getUserInterface().show("Патруль отправился в "+school);
    }

    @Override
    public State next(Context context) {
        ((PublicSafetyDepartmentContext) context).setNext(new InitialState());
        return null;
    }
}

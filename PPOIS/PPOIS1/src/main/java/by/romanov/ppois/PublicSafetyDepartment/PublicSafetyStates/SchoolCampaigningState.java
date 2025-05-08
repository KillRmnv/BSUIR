package by.romanov.ppois.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.Department;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.State;

public class SchoolCampaigningState implements State {
    @Override
    public void run(Context context) {
        PublicSafetyDepartmentContext publicSafetyDepartmentContext = (PublicSafetyDepartmentContext) context;
        PublicSafetyDepartmentInput pubSafeInput=new PublicSafetyDepartmentInput(publicSafetyDepartmentContext.getInput());
        int choice=pubSafeInput.chooseSchool();
        String school="Школа №"+choice;
        context.getUserInterface().show("Патруль отправился в "+school);
    }

    @Override
    public State next(Context context) {
        ((PublicSafetyDepartmentContext) context).setNext(new InitialState());
        return null;
    }
}

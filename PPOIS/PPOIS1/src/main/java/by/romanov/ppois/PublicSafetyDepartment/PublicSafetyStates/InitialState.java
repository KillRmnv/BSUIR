package by.romanov.ppois.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.State;

public class InitialState implements State {
    @Override
    public void run(Context context) {

    }

    @Override
    public State next(Context context) {
        PublicSafetyDepartmentInput punSafeInput=new PublicSafetyDepartmentInput( context.getInput());
       switch( punSafeInput.chooseOption()){
           case 1->{
               return new SchoolCampaigningState();
           }
           case 2->{
               return new AreasPatrolState();
           }
       }
        return null;
    }
}

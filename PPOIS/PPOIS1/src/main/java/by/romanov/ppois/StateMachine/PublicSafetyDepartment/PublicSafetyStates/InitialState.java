package by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentInput;
import by.romanov.ppois.StateMachine.State;

public class InitialState implements State {
    @Override
    public void run(Context context) {

    }

    @Override
    public State next(Context context) throws Exception {
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

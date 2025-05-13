package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.StateMachine.Police.PoliceStates.NewCaseState;
import by.romanov.ppois.StateMachine.State;

public class ReceiveCallState implements State {
    @Override
    public  void run(Context context) {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());
        Case newCase = new Case();
        newCase.setType(input.receiveCall());
        controlCentreContext.setCurrentCase(newCase);
        controlCentreContext.setIsReceivingCall(true);

    }

    @Override
    public State next(Context context) {
        ((ControlCentreContext)context).setNextStage(new NewCaseState());
        return new ChooseLawState();
    }
}

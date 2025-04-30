package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.*;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Police.PoliceStates.NewCaseState;

public class ReceiveCallState implements State {
    @Override
    public  void run(Context context) {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());
        Case newCase = new Case();
        int type=input.receiveCall();
        newCase.setType(type);
        controlCentreContext.setCurrentCase(newCase);
        controlCentreContext.setIsReceivingCall(true);

    }

    @Override
    public State next(Context context) {
        ((ControlCentreContext)context).setNextStage(new NewCaseState());
        return new ChooseLawState();
    }
}

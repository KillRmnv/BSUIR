package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.State;

public class InitialState implements State {
    @Override
    public void run(Context context) {
    }

    @Override
    public State next(Context context) {
        ControlCentereInput input=new ControlCentereInput(((ControlCentreContext)context).getInput());

        return switch (input.chooseOptions()) {
            case 1 -> new ReceiveCallState();
            case 2 -> new ManipulatingSuspectSourceState();
            default -> null;
        };
    }
}
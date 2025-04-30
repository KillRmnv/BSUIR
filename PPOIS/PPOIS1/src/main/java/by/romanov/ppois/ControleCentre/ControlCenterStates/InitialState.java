package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.State;

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
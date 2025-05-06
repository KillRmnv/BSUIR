package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.*;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Police.PoliceStates.InitialState;

public class ManipulatingSuspectSourceState implements State {
    @Override
    public void run(Context context) {
    }
    @Override
    public State next(Context context) {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        switch (input.chooseDbAction()) {
            case 1:
                input.show(((ControlCentreContext) context).getSuspectSource().getSuspects());
                break;
            case 2:
                return  new DeleteSuspectState();
            case 3:
                return new DescribingAgeState();

        }
        ((ControlCentreContext) context).setNextStage(new InitialState());
        return null;
    }
}
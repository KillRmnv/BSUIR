package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;

public class ManipulatingSuspectSourceState implements State {
    @Override
    public void run(Context context) {
    }
    @Override
    public State next(Context context) throws IOException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        switch (input.chooseSourceAction()) {
            case 1:
                input.show(((ControlCentreContext) context).getControlCentreService().getSuspectRepository().loadAll().getSuspects(), context.getUserInterface());
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
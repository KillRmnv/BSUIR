package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

public class DeleteSuspectState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        String choice = input.fullName();
        controlCentreContext.getUserInterface().show(controlCentreContext.getControlCentreService().deleteSuspect(choice));
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ((ControlCentreContext) context).setNextStage(new InitialState());
        return null;
    }
}

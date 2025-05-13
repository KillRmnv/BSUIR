package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.State;

import java.lang.reflect.InvocationTargetException;

public class DescribingAgeState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        var traits = controlCentreContext.getTransfer().getTraits();
        if (controlCentreContext.getIsReceivingCall()) {
            traits.setAge(input.age());
        } else {
            traits.setAge(input.exactAge());
        }
        context.getTransfer().setTraits(traits);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new DescribingHeightState();
    }
}

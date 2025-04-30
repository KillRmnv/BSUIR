package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.State;

import java.lang.reflect.InvocationTargetException;

public class DescribingWeightState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        var traits = controlCentreContext.getTransfer().getTraits();
        if (controlCentreContext.getIsReceivingCall()) {
            traits.setWeight(input.weight());
        } else
            traits.setWeight(input.exactWeight());
        context.getTransfer().setTraits(traits);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new DescribingHairColorState();
    }
}

package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.State;

import java.lang.reflect.InvocationTargetException;

public class ChooseLawState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());
        var newCase=controlCentreContext.getCurrentCase();
        newCase.setLaw(input.chooseLaw(newCase.getType(),controlCentreContext.getLawRegistry()));
        controlCentreContext.setCurrentCase(newCase);
        //controlCentreContext.getTransfer().setCaseData(newCase);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new ContactsState();
    }
}

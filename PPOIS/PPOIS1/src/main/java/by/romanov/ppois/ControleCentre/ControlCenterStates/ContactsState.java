package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.State;

import java.lang.reflect.InvocationTargetException;

public class ContactsState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());
        var newCase=controlCentreContext.getTransfer().getCaseData();
        newCase.setContacts(input.witnessContactData());
        controlCentreContext.setCurrentCase(newCase);
       // controlCentreContext.getTransfer().setCaseData(newCase);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new DescribingAgeState();
    }
}

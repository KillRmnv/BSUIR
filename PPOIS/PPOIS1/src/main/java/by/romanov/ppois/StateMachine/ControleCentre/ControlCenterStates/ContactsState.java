package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.State;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class ContactsState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());
        var newCase=controlCentreContext.getTransfer().getCaseData();
        List<String> choice = input.witnessContactData();
        newCase.setContacts(choice);
        controlCentreContext.setCurrentCase(newCase);
       // controlCentreContext.getTransfer().setCaseData(newCase);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new DescribingAgeState();
    }
}

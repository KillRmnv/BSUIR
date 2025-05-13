package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

public class ChooseLawState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        ControlCentereInput input=new ControlCentereInput( controlCentreContext.getInput());

        var newCase=controlCentreContext.getCurrentCase();
        Law choice = input.chooseLaw(newCase.getType(),controlCentreContext.getControlCentreService().getLawRepository().loadAll(),context.getUserInterface());
        newCase.setLaw(choice);
        controlCentreContext.setCurrentCase(newCase);
        //controlCentreContext.getTransfer().setCaseData(newCase);
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        return new ContactsState();
    }
}

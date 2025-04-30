package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.State;

import java.lang.reflect.InvocationTargetException;

public class DeleteSuspectState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
      if(!((ControlCentreContext) context).getSuspectSource().deleteSuspect(input.fullName())){
          input.noSuchSuspect();
      }
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ((ControlCentreContext)context).setNextStage(new InitialState());
        return null;
    }
}

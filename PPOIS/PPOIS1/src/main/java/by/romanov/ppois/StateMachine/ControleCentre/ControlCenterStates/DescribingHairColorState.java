package by.romanov.ppois.StateMachine.ControleCentre.ControlCenterStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentereInput;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.Police.PoliceStates.NewCaseState;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

public class DescribingHairColorState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        var traits = controlCentreContext.getTransfer().getTraits();

        controlCentreContext.getControlCentreService().describeHairColor(context.getTransfer().getCaseData(),traits,
                controlCentreContext.getIsReceivingCall(), SuspectSource.traitStringHair(input.describeHairColor()));
    }

    @Override
    public State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        if (((ControlCentreContext) context).getIsReceivingCall()) {
            ((ControlCentreContext) context).setNextStage(new NewCaseState());
            ((ControlCentreContext) context).setIsReceivingCall(false);
        } else
            ((ControlCentreContext) context).setNextStage(new InitialState());
        return null;
    }
}

package by.romanov.ppois.ControleCentre.ControlCenterStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.ControleCentre.ControlCentereInput;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.Police.PoliceStates.NewCaseState;
import by.romanov.ppois.State;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;

import java.lang.reflect.InvocationTargetException;

public class DescribingHairColorState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        ControlCentereInput input = new ControlCentereInput(((ControlCentreContext) context).getInput());
        ControlCentreContext controlCentreContext = (ControlCentreContext) context;
        var traits = controlCentreContext.getTransfer().getTraits();
        traits.setHairColor(SuspectSource.traitStringHair(input.describeHairColor()));
        if (controlCentreContext.getIsReceivingCall()) {
            controlCentreContext.getTransfer().getCaseData().setCommonTraits(traits);
        } else {
            Suspect suspect = new Suspect();
            suspect.setTraits(traits);
            controlCentreContext.getSuspectSource().addSuspect(suspect);
        }
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

package by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentStates;

import by.romanov.ppois.*;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.Police.PoliceStates.PoliceManDeathState;

import java.lang.reflect.InvocationTargetException;
import java.util.Random;

public class CatchingSuspectState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        EnforcementDepartmentContext contextEnforcementDepartment = (EnforcementDepartmentContext) context;
        EnforcementDepartmentInput input=new EnforcementDepartmentInput( contextEnforcementDepartment.getInput());
        if(!contextEnforcementDepartment.getCases().isEmpty()) {
            Case currCase = contextEnforcementDepartment.getCases().get(contextEnforcementDepartment.getChoice());
            Suspect suspect = currCase.getSuspects().getFirst();
            int numPoliceMan = input.
                    choosePoliceMan(contextEnforcementDepartment.getPoliceMans());
            contextEnforcementDepartment.setPoliceMan(numPoliceMan);


            PoliceMan policeMan = contextEnforcementDepartment.getPoliceMans().get(numPoliceMan);
            int decreaseInChance = 0;
            if (input.chooseAction() == 1) {
                input.qteMessage();
                if (context.getInput().handleQTE()) {
                    input.successQTE();
                    decreaseInChance = -1;
                }else{
                    input.failureQTE();
                }
            }

            while (input.askForRepeat() == 1) {
                int currTry = tryToCatch(policeMan, suspect, decreaseInChance, context);
                if (currTry == 0) {
                    decreaseInChance++;
                    input.Failure();
                } else if (currTry == 1) {
                    input.Success();
                    input.suspectCaught(currCase.getLaw());
                    contextEnforcementDepartment.delCase(contextEnforcementDepartment.getChoice());
                    return;
                } else {
                    input.deathOfPoliceman();
                    contextEnforcementDepartment.setNextStage(new PoliceManDeathState());
                    return;
                }
            }
            input.suspectEscaped();
            contextEnforcementDepartment.delCase(contextEnforcementDepartment.getChoice());
        }else{
            input.noCaseMessage();
        }
    }


    @Override
    public State next(Context context) {
        return null;
    }

    private int tryToCatch(PoliceMan policeMan, Suspect suspect, int decreaseInChance,Context context) {
        double randomFactor = 1 + (Math.random() * 0.2 - 0.1);
        double chance = ((double) policeMan.getExperience() / (policeMan.getExperience() + suspect.getIntellegence())) * 100 * randomFactor;
        chance = chance + decreaseInChance * (chance * 0.05);
        Random random = new Random();
        double tryToCatch = random.nextDouble(100);
        if (tryToCatch > chance) {
            return 1;
        } else if (tryToCatch > chance * 0.2) {
            return 0;
        } else {
            ((EnforcementDepartmentInput) context.getInput()).qteMessageCriticFailure();
            if (context.getInput().handleQTE()) {
                return 0;
            }
            return -1;
        }
    }
}
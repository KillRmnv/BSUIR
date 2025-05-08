package by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentStates;

import by.romanov.ppois.*;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Police.PoliceStates.PoliceManDeathState;

import java.lang.reflect.InvocationTargetException;
import java.util.Random;

public class CatchingSuspectState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        EnforcementDepartmentContext contextEnforcementDepartment = (EnforcementDepartmentContext) context;
        EnforcementDepartmentInput input = new EnforcementDepartmentInput(contextEnforcementDepartment.getInput());
        if (!contextEnforcementDepartment.getCases().isEmpty()) {
            Case currCase = contextEnforcementDepartment.getCases().get(contextEnforcementDepartment.getChoice());
            Suspect suspect = currCase.getSuspects().getFirst();
            int numPoliceMan = input.
                    choosePoliceMan(contextEnforcementDepartment.getPoliceMans());
            contextEnforcementDepartment.setPoliceMan(numPoliceMan);
            PoliceMan policeMan = contextEnforcementDepartment.getPoliceMans().get(numPoliceMan);
            int decreaseInChance = 0;
            if (input.chooseAction() == 1) {
                contextEnforcementDepartment.getUserInterface().show("Критическая ситуация:быстро нажмите ПРОБЕЛ (у вас 2 секунды)!");
                if (context.getInput().handleQTE()) {
                    contextEnforcementDepartment.getUserInterface().show("Шанс поимки увеличен!");
                    decreaseInChance = -1;
                } else {
                    contextEnforcementDepartment.getUserInterface().show("Вы не успели");
                }
            }

            while (input.askForRepeat() == 1) {
                int currTry = tryToCatch(policeMan, suspect, decreaseInChance, context);
                if (currTry == 0) {
                    decreaseInChance++;
                    contextEnforcementDepartment.getUserInterface().show("Преступник ускользнул!");

                } else if (currTry == 1) {
                    contextEnforcementDepartment.getUserInterface().show("Преступник пойман!");
                    contextEnforcementDepartment.getUserInterface().show("""
                            Преступник пойман и наказан:
                            """ + currCase.getLaw().getPunishment());

                    contextEnforcementDepartment.delCase(contextEnforcementDepartment.getChoice());
                    return;
                } else {
                    contextEnforcementDepartment.getUserInterface().show("Критический провал:полицейский убит,преступник ускользнул!")
                    ;

                    contextEnforcementDepartment.setNextStage(new PoliceManDeathState());
                    return;
                }
            }
            contextEnforcementDepartment.getUserInterface().show("Преступник скрылся. Дело отправлено в архив");

            contextEnforcementDepartment.delCase(contextEnforcementDepartment.getChoice());
        } else {
            contextEnforcementDepartment.getUserInterface().show("Дел нет");

        }
    }


    @Override
    public State next(Context context) {
        return null;
    }

    private int tryToCatch(PoliceMan policeMan, Suspect suspect, int decreaseInChance, Context context) {
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
            context.getUserInterface().show("Критическая ситуация:быстро нажмите ПРОБЕЛ (у вас 2 секунды)!");

            if (context.getInput().handleQTE()) {
                return 0;
            }
            return -1;
        }
    }
}
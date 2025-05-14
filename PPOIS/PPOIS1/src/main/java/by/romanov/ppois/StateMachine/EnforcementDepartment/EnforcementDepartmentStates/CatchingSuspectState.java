package by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentStates;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.concurrent.atomic.AtomicInteger;

public class CatchingSuspectState implements State {
    @Override
    public void run(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException, IOException {
        EnforcementDepartmentContext contextEnforcementDepartment = (EnforcementDepartmentContext) context;
        EnforcementDepartmentInput input = new EnforcementDepartmentInput(contextEnforcementDepartment.getInput());

        Case currCase = contextEnforcementDepartment.getTransfer().getCaseData();
        var map=contextEnforcementDepartment.getPoliceManRepository().loadAll();
        contextEnforcementDepartment.getUserInterface().showMap(map,"Выберите полицейского:");
        int numPoliceMan = input.
                choosePoliceMan(map);
        contextEnforcementDepartment.setPoliceMan(numPoliceMan);
        PoliceMan policeMan = contextEnforcementDepartment.getPoliceManRepository().loadAll().get(numPoliceMan);
        AtomicInteger decreaseInChance =new AtomicInteger( 0);
        int choice = input.chooseAction();
        if (choice == 1) {
            contextEnforcementDepartment.getUserInterface().show("Критическая ситуация:быстро нажмите ПРОБЕЛ (у вас 2 секунды)!");
            if (context.getInput().handleQTE()) {
                contextEnforcementDepartment.getUserInterface().show("Шанс поимки увеличен!");
                decreaseInChance.set(-1);
            } else {
                contextEnforcementDepartment.getUserInterface().show("Вы не успели");
            }
        }
        choice=1;
        while (choice == 1) {
            contextEnforcementDepartment.getUserInterface().show(contextEnforcementDepartment.getEnforcementService().
                    catchSuspect(currCase, policeMan, decreaseInChance));
            if(decreaseInChance.get()<-1)
                break;
            choice = input.askForRepeat();
        }
    }

    @Override
    public State next(Context context) {
        return null;
    }
}
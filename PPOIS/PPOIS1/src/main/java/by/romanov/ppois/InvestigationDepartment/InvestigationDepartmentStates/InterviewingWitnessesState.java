package by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentStates;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentInput;
import by.romanov.ppois.Police.PoliceStates.NewEnforcementDepartmentCaseState;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class InterviewingWitnessesState implements State {
    @Override
    public void run(Context context) {
        InvestigationDepartmentContext investigationDepartmentContext = (InvestigationDepartmentContext) context;
        InvestigationDepartmentInput input = new InvestigationDepartmentInput(investigationDepartmentContext.getInput());
        Case currentCase = investigationDepartmentContext.getCurrentCase();
        List<Traits> witnessTraits = new ArrayList<>();
        List<String> contacts = currentCase.getContacts();
        for (var contact : contacts) {
            Traits newTrait = new Traits(true);
            context.getUserInterface().show("Цвет волос: "+newTrait.getHairColor());
            context.getUserInterface().showNumericRange("Вес: ", newTrait.getWeight() / 1000, newTrait.getWeight() % 1000);
            context.getUserInterface().showNumericRange("Рост: ", newTrait.getHeight() / 1000, newTrait.getHeight() % 1000);
            context.getUserInterface().showNumericRange("Возраст: ", newTrait.getAge() / 100, newTrait.getAge() % 100);
            witnessTraits.add(newTrait);
        }
        AtomicInteger maxWitnesses = new AtomicInteger(0);
        AtomicInteger maxUser = new AtomicInteger(0);
        Set<Suspect> witnessSuspects = investigationDepartmentContext.
                getSuspectSource().findSuspectsBasedOnCommonTraits(witnessTraits, maxWitnesses);
        Set<Suspect> userSuspects = investigationDepartmentContext.
                getSuspectSource().findSuspectsBasedOnCommonTraits(new ArrayList<>(Collections.singletonList(currentCase.getCommonTraits())), maxUser);
        if ((double) maxWitnesses.get() > (double)maxUser.get() * 1.5) {
            userSuspects = SuspectSource.intersection(witnessSuspects, userSuspects);
            if (!userSuspects.isEmpty()) {
                currentCase.setSuspects(new ArrayList<>(Collections.singletonList(userSuspects.iterator().next())));
            } else if (!witnessSuspects.isEmpty()) {
                currentCase.setSuspects(new ArrayList<>(Collections.singletonList(witnessSuspects.iterator().next())));
            } else {
                currentCase.setSuspects(null);
            }

        } else {
            witnessSuspects = SuspectSource.intersection(witnessSuspects, userSuspects);
            if (!witnessSuspects.isEmpty()) {
                currentCase.setSuspects(new ArrayList<>(Collections.singletonList(witnessSuspects.iterator().next())));
            } else if (!userSuspects.isEmpty()) {
                currentCase.setSuspects(new ArrayList<>(Collections.singletonList(userSuspects.iterator().next())));
            } else {
                currentCase.setSuspects(null);
            }
        }
    }

    @Override
    public State next(Context context) {
        ((InvestigationDepartmentContext) context).getTransfer().setCaseData(((InvestigationDepartmentContext) context).getCurrentCase());
        ((InvestigationDepartmentContext) context).setChoice(new NewEnforcementDepartmentCaseState());
        return null;
    }
}

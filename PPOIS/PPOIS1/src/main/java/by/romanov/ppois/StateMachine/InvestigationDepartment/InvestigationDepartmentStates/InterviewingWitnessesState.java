package by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentStates;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class InterviewingWitnessesState implements State {
    @Override
    public void run(Context context) throws IOException {
        InvestigationDepartmentContext investigationDepartmentContext = (InvestigationDepartmentContext) context;
        Case currentCase = investigationDepartmentContext.getTransfer().getCaseData();
        List<Traits> witnessTraits = new ArrayList<>();
        List<String> contacts = currentCase.getContacts();
        for (var contact : contacts) {
            Traits newTrait = new Traits(true);
            context.getUserInterface().show(contact);
            context.getUserInterface().show("Цвет волос: "+newTrait.getHairColor());
            context.getUserInterface().showNumericRange("Вес: ", newTrait.getWeight() / 1000, newTrait.getWeight() % 1000);
            context.getUserInterface().showNumericRange("Рост: ", newTrait.getHeight() / 1000, newTrait.getHeight() % 1000);
            context.getUserInterface().showNumericRange("Возраст: ", newTrait.getAge() / 100, newTrait.getAge() % 100);
            witnessTraits.add(newTrait);
        }
        investigationDepartmentContext.getInvestigationService().interviewWitnesses(currentCase, witnessTraits);
    }

    @Override
    public State next(Context context) {
        ((InvestigationDepartmentContext) context).setChoice(new InitialState());
        return null;
    }
}

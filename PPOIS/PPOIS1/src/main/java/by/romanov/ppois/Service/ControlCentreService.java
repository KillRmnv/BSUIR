package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.*;

import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Repository.SuspectSourceJsonRepository;

import lombok.Data;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.List;
@Data
public class ControlCentreService {
    protected final Repository<LawRegistry, Law,Law> lawRepository;
    protected final Repository<SuspectSource, Suspect, String> suspectRepository;
    public ControlCentreService() {
        lawRepository=new LawRegistryJsonRepository();
        suspectRepository=new SuspectSourceJsonRepository();
    }
    public ControlCentreService(  Repository<LawRegistry, Law,Law> lawRepository, Repository<SuspectSource, Suspect, String> suspectRepository) {
        this.lawRepository = lawRepository;
        this.suspectRepository = suspectRepository;
    }

    public void receiveCall(Case newCase, Integer caseType) {
        newCase.setType(caseType);
    }



    public void setWitnessContacts(Case newCase, List<String> contacts) {
        newCase.setContacts(contacts);
    }

    public void describeAge(Traits traits, boolean isReceivingCall, int age, int exactAge) {
        if (isReceivingCall) {
            traits.setAge(age);
        } else {
            traits.setAge(exactAge);
        }
    }

    public void describeHeight(Traits traits, boolean isReceivingCall, int height, int exactHeight) {
        if (isReceivingCall) {
            traits.setHeight(height);
        } else {
            traits.setHeight(exactHeight);
        }
    }

    public void describeWeight(Traits traits, boolean isReceivingCall, int weight, int exactWeight) {
        if (isReceivingCall) {
            traits.setWeight(weight);
        } else {
            traits.setWeight(exactWeight);
        }
    }

    public void describeHairColor(Case newCase, Traits traits, boolean isReceivingCall, String hairColor) throws IOException {
        traits.setHairColor(hairColor);
        if (isReceivingCall) {
            newCase.setCommonTraits(traits);
        } else {
            Suspect suspect = new Suspect();
            suspect.setTraits(traits);
            suspectRepository.add(suspect);
            return;
        }
    }


    public String deleteSuspect(String fullName) throws IOException {
        Suspect suspect = new Suspect();
        suspect.setName(fullName);
        if (!suspectRepository.delete(suspect)) {
            return "Такого подозреваемого нет";
        } else {
            return "Список подозреваемых обновлен";
        }
    }

    public LawRegistry getAvailableLaws() throws IOException {
        return lawRepository.loadAll();
    }

    public SuspectSource getSuspectSource() throws IOException {
        return suspectRepository.loadAll();
    }
}
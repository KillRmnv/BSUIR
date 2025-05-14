package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.*;

import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Repository.SuspectSourceJsonRepository;

import lombok.Data;

import java.io.IOException;

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
        suspect.setFullName(fullName);
        if (!suspectRepository.delete(suspect)) {
            return "Такого подозреваемого нет";
        } else {
            return "Список подозреваемых обновлен";
        }
    }

}
package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Repository.CaseJsonRepository;
import by.romanov.ppois.Repository.PoliceMansJsonRepository;
import by.romanov.ppois.Repository.Repository;
import lombok.Data;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;
@Data
public class EnforcementService {
    protected final Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> policeManRepository;
    protected final Repository<List<Case>, Case, Integer> caseRepository;
    public EnforcementService(Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> policeManRepository, Repository<List<Case>, Case, Integer> caseRepository){
        this.policeManRepository = policeManRepository;
        this.caseRepository = caseRepository;
    }
    public EnforcementService() {
        this.policeManRepository = new PoliceMansJsonRepository();
        this.caseRepository = new CaseJsonRepository();
    }

    public String catchSuspect(Case currCase, PoliceMan policeMan, AtomicInteger decreaseInChance) throws IOException {
        Suspect suspect = currCase.getSuspects().getFirst();

        int result = tryToCatch(policeMan, suspect, decreaseInChance);
        if(result == 0){
            decreaseInChance.addAndGet(1);
            return  "Преступник ускользнул!";
        }else
        if (result == 1) {
            caseRepository.delete(currCase);

            String res= "Преступник пойман и наказан: " + currCase.getLaw().getPunishment();
            decreaseInChance.set(-2);
            return res;
        } else if (result == -1) {
            policeManRepository.delete(policeMan);
            decreaseInChance.set(-2);
            return "Критический провал: полицейский убит, преступник скрылся!";
        } else {
            caseRepository.delete(currCase);
            decreaseInChance.set(-2);
            return "Преступник скрылся. Дело архивировано.";
        }
    }

    public int tryToCatch(PoliceMan policeMan, Suspect suspect, AtomicInteger decreaseInChance) {
        double randomFactor = 1 + (Math.random() * 0.2 - 0.1);
        double chance = ((double) policeMan.getExperience() / (policeMan.getExperience() + suspect.getIntellegence())) * 100 * randomFactor;
        chance = chance + decreaseInChance.get() * (chance * 0.05);
        Random random = new Random();
        double tryToCatch = random.nextDouble(100);
        if (tryToCatch > chance) {
            return 1;
        } else if (tryToCatch > chance * 0.2) {
            return 0;
        } else {
            return -1;
        }
    }

    public HashMap<Integer, PoliceMan> getAvailablePoliceMen() throws IOException {
        return policeManRepository.loadAll();
    }

    public List<Case> getActiveCases() throws IOException {
        return caseRepository.loadAll();
    }
}

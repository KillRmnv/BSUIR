package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Repository.PoliceMansJsonRepository;
import by.romanov.ppois.Repository.Repository;
import lombok.Data;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.*;

@Data
public class HRService {
    protected final Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> policeManRepository;
    protected double budget;
    public HRService() {
        policeManRepository=new PoliceMansJsonRepository();
    }
    public HRService(Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> policeManRepository) {
        this.policeManRepository = policeManRepository;
        this.budget = 10000;
    }

    public String firePoliceMan(int policeManIndex) throws IOException {
        List<PoliceMan> policeManList = new ArrayList<>(policeManRepository.loadAll().values());
        if (policeManIndex >= 0 && policeManIndex < policeManList.size()) {
            PoliceMan policeMan = policeManList.get(policeManIndex);
            policeManRepository.delete(policeMan);
            budget += policeMan.getSalary();

            return "Полицейский уволен. Бюджет: " + budget;
        }
        return "";
    }

    public String hirePoliceMan(int policeManIndex, HashMap<Integer, PoliceMan> newPoliceMans) throws IOException, InvocationTargetException, NoSuchMethodException, IllegalAccessException {
       // userInterface.showMap(newPoliceMans,"Выберите полицейского для найма");
        if (newPoliceMans.containsKey(policeManIndex)) {
            PoliceMan policeMan = newPoliceMans.get(policeManIndex);
            if (budget >= policeMan.getSalary()) {
                policeManRepository.add(policeMan);
                budget -= policeMan.getSalary();
                return "Полицейский нанят. Бюджет: " + budget;
            } else {
               return "Недостаточно бюджета для найма";
            }
        }
        return "";
    }

    public HashMap<Integer, PoliceMan> generateNewPoliceMans() throws IOException {
        HashMap<Integer, PoliceMan> newPoliceMans = new LinkedHashMap<>();
        Random random = new Random();
        HashMap<Integer, PoliceMan> existingPoliceMans = policeManRepository.loadAll();
        for (int index = 0; index < 10; index++) {
            int randomId = random.nextInt();
            while (existingPoliceMans.containsKey(randomId)) {
                randomId = random.nextInt();
            }
            PoliceMan newOne = new PoliceMan(randomId);
            newPoliceMans.put(index, newOne);
        }
        return newPoliceMans;
    }

    public HashMap<Integer, PoliceMan> getAvailablePoliceMans() throws IOException {
        return policeManRepository.loadAll();
    }

    public double getBudget() {
        return budget;
    }
}
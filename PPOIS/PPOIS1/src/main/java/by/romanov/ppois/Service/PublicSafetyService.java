package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import by.romanov.ppois.Repository.Repository;

import lombok.Data;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
@Data
public class PublicSafetyService {
    protected final Repository<LawRegistry, Law,Law> lawRegistry;
    protected final List<String> areas = new ArrayList<>(Arrays.asList(
            "Советский", "Центральный", "Первомайский", "Партизанский", "Заводской",
            "Ленинский", "Октябрьский", "Московский", "Фрунзенский"));
    public PublicSafetyService(){
        lawRegistry = new LawRegistryJsonRepository();
    }

    public PublicSafetyService(Repository<LawRegistry, Law,Law> lawRegistry) {
        this.lawRegistry = lawRegistry;
    }

    public Case checkForCrime() throws IOException {
        Random crime = new Random();
        if (crime.nextInt(100) < 60) {
            return new Case(lawRegistry.loadAll().getCRIMINAL_LAWS());
        }
        return null;
    }


    public List<String> getAreas() {
        return areas;
    }
}
package by.romanov.ppois.Repository;

import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class LawRegistryJsonRepository implements Repository<LawRegistry, Law,Law> {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());
    private static  String FILE_PATH = "./src/main/resources/law_registry.json";
    private LawRegistry lawRegistry;

    public LawRegistryJsonRepository() {
        this.lawRegistry = new LawRegistry();
    }
    public LawRegistryJsonRepository(String file) {
        FILE_PATH=file;
    }

    @Override
    public void saveAll(LawRegistry lawRegistry) throws IOException {
        objectMapper.writeValue(new File(FILE_PATH), lawRegistry);
    }

    @Override
    public LawRegistry loadAll() throws IOException {
        File file = new File(FILE_PATH);
        if (file.exists()) {
            lawRegistry = objectMapper.readValue(file, LawRegistry.class);
        } else {
            lawRegistry = new LawRegistry();
            saveAll(lawRegistry);
        }
        return lawRegistry;
    }

    @Override
    public boolean delete(Law law) throws IOException {
        HashMap<Integer, Law> criminalLaws = lawRegistry.getCRIMINAL_LAWS();
        if (criminalLaws.containsKey(law.getId()) && criminalLaws.get(law.getId()).equals(law)) {
            criminalLaws.remove(law.getId());
            saveAll(lawRegistry);
            return true;
        } else {
            HashMap<Integer, Law> adminLaws = lawRegistry.getADMIN_LAWS();
            if (adminLaws.containsKey(law.getId()) && adminLaws.get(law.getId()).equals(law)) {
                adminLaws.remove(law.getId());
                saveAll(lawRegistry);
                return true;
            }
        }

        return false;
    }


    @Override
    public void add(Law law) throws IOException {
        if (law.getType().equals("CRIMINAL")) {
            HashMap<Integer, Law> criminalLaws = lawRegistry.getCRIMINAL_LAWS();
            criminalLaws.put(law.getId(), law);
            lawRegistry.setCRIMINAL_LAWS(criminalLaws);
        } else if (law.getType().equals("ADMIN")) {
            HashMap<Integer, Law> adminLaws = lawRegistry.getADMIN_LAWS();
            adminLaws.put(law.getId(), law);
            lawRegistry.setADMIN_LAWS(adminLaws);
        } else {
            throw new IllegalArgumentException("Тип закона должен быть 'CRIMINAL' или 'ADMIN'");
        }
        saveAll(lawRegistry);
    }

    @Override
    public Law load(Law law) throws IOException {
        if(law.getType().equals("ADMIN")) {
            Map<Integer, Law> adminLaws = lawRegistry.getADMIN_LAWS();
            if(adminLaws.containsKey(law.getId())) {
                return adminLaws.get(law.getId());
            }
        }else {
            Map<Integer,Law> criminalLaws=lawRegistry.getCRIMINAL_LAWS();
            if(criminalLaws.containsKey(law.getId())) {
                return criminalLaws.get(law.getId());
            }
        }
        return null;
    }
}
package by.romanov.ppois.Repository;

import by.romanov.ppois.Entities.PoliceMan;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

public class PoliceMansJsonRepository implements Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());
    private static final String FILE_PATH = "./src/main/resources/police_mans.json";
    private HashMap<Integer, PoliceMan> policeMans;

    public PoliceMansJsonRepository() {
        this.policeMans = new HashMap<>();
    }

    @Override
    public void saveAll(HashMap<Integer, PoliceMan> data) throws IOException {
        this.policeMans = data;
        objectMapper.writeValue(new File(FILE_PATH), policeMans);
    }

    @Override
    public HashMap<Integer, PoliceMan> loadAll() throws IOException {
        File file = new File(FILE_PATH);
        if (file.exists()) {
            policeMans = objectMapper.readValue(file, objectMapper.getTypeFactory()
                    .constructMapType(HashMap.class, Integer.class, PoliceMan.class));
        } else {
            policeMans = new HashMap<>();
        }
        return policeMans;
    }

    @Override
    public boolean delete(PoliceMan policeMan) throws IOException {
        policeMans.remove(policeMan.getId());
        saveAll(policeMans);
        return false;
    }

    @Override
    public void add(PoliceMan policeMan) throws IOException {
        policeMan.setId(policeMans.size());
        policeMans.put(policeMans.size(), policeMan);
        saveAll(policeMans);
    }

    @Override
    public PoliceMan load(Integer key) throws IOException {
        return policeMans.get(key);
    }
}
package by.romanov.ppois.Repository;

import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class SuspectSourceJsonRepository implements Repository<SuspectSource, Suspect, String> {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());
    private static  String FILE_PATH = "./src/main/resources/suspect_source.json";
    private SuspectSource suspectSource;

    public SuspectSourceJsonRepository() {
        this.suspectSource = new SuspectSource();
    }

    public SuspectSourceJsonRepository(String filePath) {
        FILE_PATH = filePath;

    }

    @Override
    public void saveAll(SuspectSource suspectSource) throws IOException {
        this.suspectSource = suspectSource;
        objectMapper.writeValue(new File(FILE_PATH), suspectSource.getSuspects());
    }

    @Override
    public SuspectSource loadAll() throws IOException {
        File file = new File(FILE_PATH);
        if (file.exists()) {
            Map<String, Suspect> suspects = objectMapper.readValue(file, objectMapper.getTypeFactory()
                    .constructMapType(HashMap.class, String.class, Suspect.class));
            suspectSource = new SuspectSource();
            suspectSource.setSuspects(suspects);
            suspects.forEach((fullName, suspect) -> suspectSource.addSuspect(suspect));
        } else {
            suspectSource = new SuspectSource();
            initData();
            saveAll(suspectSource);
        }
        return suspectSource;
    }

    @Override
    public boolean delete(Suspect suspect) throws IOException {
        suspectSource=loadAll();
        int size=suspectSource.getSuspects().size();
        suspectSource.deleteSuspect(suspect.getFullName());
        if(size==suspectSource.getSuspects().size()){
            return false;
        }
        saveAll(suspectSource);
        return true;
    }

    @Override
    public void add(Suspect suspect) throws IOException {
        if(suspectSource.getSuspects().isEmpty()){
            suspectSource=loadAll();
        }
        suspectSource.addSuspect(suspect);
        saveAll(suspectSource);
    }

    @Override
    public Suspect load(String key) throws IOException {
        if(suspectSource.getSuspects().isEmpty()){
            suspectSource=loadAll();
        }
        return suspectSource.getSuspects().get(key);
    }

    private void initData() {
        for (int i = 0; i < 30; i++) {
            Suspect suspect = new Suspect();
            suspectSource.addSuspect(suspect);
        }
    }
}
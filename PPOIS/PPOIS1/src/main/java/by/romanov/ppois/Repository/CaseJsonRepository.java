package by.romanov.ppois.Repository;

import by.romanov.ppois.Entities.Case;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CaseJsonRepository implements Repository<List<Case>, Case,Integer> {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());
    private static String FILE_PATH = "./src/main/resources/casesInvestigationDepartment.json";
    private List<Case> cases;

    public CaseJsonRepository() {
        this.cases = new ArrayList<>();
    }

    public CaseJsonRepository(String file) {
        FILE_PATH=file;
    }

    @Override
    public void saveAll(List<Case> list) throws IOException {
        this.cases = list;
        objectMapper.writeValue(new File(FILE_PATH), cases);
    }

    @Override
    public List<Case> loadAll() throws IOException {
        File file = new File(FILE_PATH);
        if (file.exists()) {
            cases = objectMapper.readValue(file, objectMapper.getTypeFactory()
                    .constructCollectionType(List.class, Case.class));
        } else {
            cases = new ArrayList<>();
        }
        return cases;
    }

    @Override
    public boolean delete(Case aCase) throws IOException {
        int size=cases.size();
        cases.remove(aCase);
        if(cases.size()==size){
            return false;
        }
        saveAll(cases);
        return true;
    }

    @Override
    public void add(Case data) throws IOException {
        cases.add(data);
        saveAll(cases);
    }

    @Override
    public Case load(Integer integer) throws IOException {
        return cases.get(integer);
    }
}
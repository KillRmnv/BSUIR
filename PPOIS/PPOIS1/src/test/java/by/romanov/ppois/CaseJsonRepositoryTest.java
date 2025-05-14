package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Repository.CaseJsonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class CaseJsonRepositoryTest {
    private CaseJsonRepository repository;
    private File tempFile;

    @TempDir
    File tempDir;

    @BeforeEach
    void setUp() {
        tempFile = new File(tempDir, "test_cases1.json");
        repository = new CaseJsonRepository(tempFile.getAbsolutePath());

        try {
            Field casesField = CaseJsonRepository.class.getDeclaredField("cases");
            casesField.setAccessible(true);
            casesField.set(repository, new ArrayList<Case>());
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to initialize cases field", e);
        }
    }

    @Test
    void testSaveAllAndLoadAll() throws IOException {
        List<Case> cases = new ArrayList<>();
        Case case1 = new Case();
        case1.setType(1);
        case1.getContacts().add("+123456789");
        Case case2 = new Case();
        case2.setType(2);
        case2.getContacts().add("+987654321");
        cases.add(case1);
        cases.add(case2);

        repository.add(case1);
        repository.add(case2);

        List<Case> loadedCases = repository.loadAll();

        assertEquals(2, loadedCases.size());
        assertEquals(case1.getType(), loadedCases.get(0).getType());
        assertEquals(case1.getContacts(), loadedCases.get(0).getContacts());
        assertEquals(case2.getType(), loadedCases.get(1).getType());
        assertEquals(case2.getContacts(), loadedCases.get(1).getContacts());
    }

    @Test
    void testLoadAllEmptyFile() throws IOException {
        List<Case> loadedCases = repository.loadAll();
        assertTrue(loadedCases.isEmpty());
    }

    @Test
    void testAdd() throws IOException {
        Case newCase = new Case();
        newCase.setType(3);
        newCase.getContacts().add("+555555555");

        repository.add(newCase);

        List<Case> loadedCases = repository.loadAll();

        assertEquals(1, loadedCases.size());
        assertEquals(newCase.getType(), loadedCases.get(0).getType());
        assertEquals(newCase.getContacts(), loadedCases.get(0).getContacts());
    }

    @Test
    void testDeleteSuccess() throws IOException {
        List<Case> cases = new ArrayList<>();
        Case case1 = new Case();
        case1.setType(1);
        case1.getContacts().add("+123456789");
        Case case2 = new Case();
        case2.setType(2);
        case2.getContacts().add("+987654321");
        cases.add(case1);
        cases.add(case2);
        repository.saveAll(cases);

        boolean deleted = repository.delete(case1);

        assertTrue(deleted);
        List<Case> loadedCases = repository.loadAll();
        assertEquals(1, loadedCases.size());
        assertEquals(case2.getType(), loadedCases.get(0).getType());
        assertEquals(case2.getContacts(), loadedCases.get(0).getContacts());
    }

    @Test
    void testDeleteNonExistent() throws IOException {
        List<Case> cases = new ArrayList<>();
        Case case1 = new Case();
        case1.setType(1);
        cases.add(case1);
        repository.saveAll(cases);

        Case nonExistentCase = new Case();
        nonExistentCase.setType(2);
        boolean deleted = repository.delete(nonExistentCase);

        assertFalse(deleted);
        List<Case> loadedCases = repository.loadAll();
        assertEquals(1, loadedCases.size());
        assertEquals(case1.getType(), loadedCases.get(0).getType());
    }

    @Test
    void testLoadByIndex() throws IOException {
        List<Case> cases = new ArrayList<>();
        Case case1 = new Case();
        case1.setType(1);
        case1.getContacts().add("+123456789");
        Case case2 = new Case();
        case2.setType(2);
        case2.getContacts().add("+987654321");
        cases.add(case1);
        cases.add(case2);
        repository.saveAll(cases);

        Case loadedCase = repository.load(1);

        assertNotNull(loadedCase);
        assertEquals(case2.getType(), loadedCase.getType());
        assertEquals(case2.getContacts(), loadedCase.getContacts());
    }

    @Test
    void testLoadInvalidIndex() throws IOException {
        List<Case> cases = new ArrayList<>();
        Case case1 = new Case();
        case1.setType(1);
        cases.add(case1);
        repository.saveAll(cases);

        assertThrows(IndexOutOfBoundsException.class, () -> repository.load(10));
    }
}
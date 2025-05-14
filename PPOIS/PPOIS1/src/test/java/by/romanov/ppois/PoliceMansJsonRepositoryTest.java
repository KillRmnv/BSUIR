package by.romanov.ppois;

import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Repository.PoliceMansJsonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

public class PoliceMansJsonRepositoryTest {
    private PoliceMansJsonRepository repository;
    private File tempFile;

    @TempDir
    File tempDir;

    @BeforeEach
    void setUp() {
        tempFile = new File(tempDir, "test_police_mans.json");
        repository = new PoliceMansJsonRepository(tempFile.getAbsolutePath());

        // Initialize policeMans with an empty HashMap
        try {
            Field policeMansField = PoliceMansJsonRepository.class.getDeclaredField("policeMans");
            policeMansField.setAccessible(true);
            policeMansField.set(repository, new HashMap<Integer, PoliceMan>());
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to initialize policeMans field", e);
        }
    }

    @Test
    void testSaveAllAndLoadAll() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan1 = new PoliceMan(1);
        policeMan1.setSalary(1000);
        PoliceMan policeMan2 = new PoliceMan(2);
        policeMan2.setSalary(2000);
        policeMans.put(1, policeMan1);
        policeMans.put(2, policeMan2);

        repository.saveAll(policeMans);

        HashMap<Integer, PoliceMan> loadedPoliceMans = repository.loadAll();

        assertEquals(2, loadedPoliceMans.size());
        assertEquals(1000, loadedPoliceMans.get(1).getSalary());
        assertEquals(2000, loadedPoliceMans.get(2).getSalary());
    }

    @Test
    void testLoadAllEmptyFile() throws IOException {
        HashMap<Integer, PoliceMan> loadedPoliceMans = repository.loadAll();
        assertTrue(loadedPoliceMans.isEmpty());
    }

    @Test
    void testAdd() throws IOException {
        PoliceMan policeMan = new PoliceMan();
        policeMan.setSalary(1500);
        policeMan.setName("John");
        policeMan.setSecondName("Doe");

        repository.add(policeMan);

        HashMap<Integer, PoliceMan> loadedPoliceMans = repository.loadAll();
        assertEquals(1, loadedPoliceMans.size());
        assertEquals(1500, loadedPoliceMans.get(0).getSalary());
        assertEquals("John", loadedPoliceMans.get(0).getName());
        assertEquals("Doe", loadedPoliceMans.get(0).getSecondName());
        assertEquals(0, loadedPoliceMans.get(0).getId());
    }

    @Test
    void testDeleteSuccess() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan = new PoliceMan(1);
       repository.add(policeMan);

        boolean deleted = repository.delete(policeMan);

        assertTrue(deleted);
        HashMap<Integer, PoliceMan> loadedPoliceMans = repository.loadAll();
        assertTrue(loadedPoliceMans.isEmpty());
    }

    @Test
    void testDeleteNonExistent() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan = new PoliceMan(1);
        policeMans.put(1, policeMan);
        repository.saveAll(policeMans);

        PoliceMan nonExistent = new PoliceMan(999);
        boolean deleted = repository.delete(nonExistent);

        assertFalse(deleted);
        HashMap<Integer, PoliceMan> loadedPoliceMans = repository.loadAll();
        assertEquals(1, loadedPoliceMans.size());
        assertEquals(policeMan.getSalary(), loadedPoliceMans.get(1).getSalary());
    }

    @Test
    void testLoad() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan = new PoliceMan(1);
        policeMan.setSalary(1000);
        policeMans.put(1, policeMan);
        repository.saveAll(policeMans);

        PoliceMan loadedPoliceMan = repository.load(1);

        assertNotNull(loadedPoliceMan);
        assertEquals(1000, loadedPoliceMan.getSalary());
    }

    @Test
    void testLoadNonExistent() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan = new PoliceMan(1);
        policeMans.put(1, policeMan);
        repository.saveAll(policeMans);

        PoliceMan loadedPoliceMan = repository.load(999);

        assertNull(loadedPoliceMan);
    }

    @Test
    void testLoadCorruptedFile() throws IOException {
        java.nio.file.Files.writeString(tempFile.toPath(), "corrupted data");
        assertThrows(Exception.class, () -> repository.loadAll());
    }
}
package by.romanov.ppois;

import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

public class LawRegistryJsonRepositoryTest {
    private LawRegistryJsonRepository repository;
    private File tempFile;

    @TempDir
    File tempDir;

    @BeforeEach
    void setUp() {
        tempFile = new File(tempDir, "test_law_registry.json");
        repository = new LawRegistryJsonRepository(tempFile.getAbsolutePath());

        try {
            Field lawRegistryField = LawRegistryJsonRepository.class.getDeclaredField("lawRegistry");
            lawRegistryField.setAccessible(true);
            LawRegistry emptyRegistry = new LawRegistry();
            emptyRegistry.setCRIMINAL_LAWS(new HashMap<>());
            emptyRegistry.setADMIN_LAWS(new HashMap<>());
            lawRegistryField.set(repository, emptyRegistry);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to initialize lawRegistry field", e);
        }
    }

    @Test
    void testSaveAllAndLoadAll() throws IOException {
        LawRegistry registry = new LawRegistry();
        HashMap<Integer, Law> criminalLaws = new HashMap<>();
        criminalLaws.put(1, new Law(1, "Test Criminal Law", "Prison", "CRIMINAL"));
        HashMap<Integer, Law> adminLaws = new HashMap<>();
        adminLaws.put(1, new Law(1, "Test Admin Law", "Fine", "ADMIN"));
        registry.setCRIMINAL_LAWS(criminalLaws);
        registry.setADMIN_LAWS(adminLaws);

        repository.saveAll(registry);

        LawRegistry loadedRegistry = repository.loadAll();

        assertEquals(1, loadedRegistry.getCRIMINAL_LAWS().size());
        assertEquals("Test Criminal Law", loadedRegistry.getCRIMINAL_LAWS().get(1).getDescription());
        assertEquals(1, loadedRegistry.getADMIN_LAWS().size());
        assertEquals("Test Admin Law", loadedRegistry.getADMIN_LAWS().get(1).getDescription());
    }

    @Test
    void testLoadAllEmptyFile() throws IOException {
        LawRegistry loadedRegistry = repository.loadAll();

        assertTrue(loadedRegistry.getCRIMINAL_LAWS().isEmpty());
        assertTrue(loadedRegistry.getADMIN_LAWS().isEmpty());
    }

    @Test
    void testAddCriminalLaw() throws IOException {
        Law law = new Law(11, "New Criminal Law", "Prison 5 years", "CRIMINAL");

        repository.add(law);

        LawRegistry loadedRegistry = repository.loadAll();
        assertEquals(1, loadedRegistry.getCRIMINAL_LAWS().size());
        assertEquals("New Criminal Law", loadedRegistry.getCRIMINAL_LAWS().get(11).getDescription());
        assertTrue(loadedRegistry.getADMIN_LAWS().isEmpty());
    }

    @Test
    void testAddAdminLaw() throws IOException {
        Law law = new Law(11, "New Admin Law", "Fine 1000", "ADMIN");

        repository.add(law);

        LawRegistry loadedRegistry = repository.loadAll();
        assertEquals(1, loadedRegistry.getADMIN_LAWS().size());
        assertEquals("New Admin Law", loadedRegistry.getADMIN_LAWS().get(11).getDescription());
        assertTrue(loadedRegistry.getCRIMINAL_LAWS().isEmpty());
    }

    @Test
    void testAddInvalidLawType() {
        Law law = new Law(11, "Invalid Law", "Penalty", "INVALID");

        assertThrows(IllegalArgumentException.class, () -> repository.add(law));
    }

    @Test
    void testDeleteCriminalLawSuccess() throws IOException {
        Law law = new Law(1, "Test Criminal Law", "Prison", "CRIMINAL");
        repository.add(law);

        boolean deleted = repository.delete(law);

        assertTrue(deleted);
        LawRegistry loadedRegistry = repository.loadAll();
        assertTrue(loadedRegistry.getCRIMINAL_LAWS().isEmpty());
    }

    @Test
    void testDeleteAdminLawSuccess() throws IOException {
        Law law = new Law(1, "Test Admin Law", "Fine", "ADMIN");
       repository.add(law);

        boolean deleted = repository.delete(law);

        assertTrue(deleted);
        LawRegistry loadedRegistry = repository.loadAll();
        assertTrue(loadedRegistry.getADMIN_LAWS().isEmpty());
    }

    @Test
    void testDeleteNonExistentLaw() throws IOException {
        Law law = new Law(999, "Non-existent Law", "None", "CRIMINAL");
        boolean deleted = repository.delete(law);

        assertFalse(deleted);
        LawRegistry loadedRegistry = repository.loadAll();
        assertTrue(loadedRegistry.getCRIMINAL_LAWS().isEmpty());
        assertTrue(loadedRegistry.getADMIN_LAWS().isEmpty());
    }

    @Test
    void testLoadCriminalLaw() throws IOException {
        Law law = new Law(1, "Test Criminal Law", "Prison", "CRIMINAL");
        repository.add(law);

        Law loadedLaw = repository.load(law);

        assertNotNull(loadedLaw);
        assertEquals("Test Criminal Law", loadedLaw.getDescription());
    }

    @Test
    void testLoadAdminLaw() throws IOException {
        Law law = new Law(1, "Test Admin Law", "Fine", "ADMIN");
        repository.add(law);

        Law loadedLaw = repository.load(law);

        assertNotNull(loadedLaw);
        assertEquals("Test Admin Law", loadedLaw.getDescription());
    }

    @Test
    void testLoadNonExistentLaw() throws IOException {
        Law law = new Law(999, "Non-existent Law", "None", "CRIMINAL");
        Law loadedLaw = repository.load(law);

        assertNull(loadedLaw);
    }
}
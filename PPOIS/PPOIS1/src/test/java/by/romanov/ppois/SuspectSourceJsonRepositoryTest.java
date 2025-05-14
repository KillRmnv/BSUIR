package by.romanov.ppois;

import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.Repository.SuspectSourceJsonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class SuspectSourceJsonRepositoryTest {
    private SuspectSourceJsonRepository repository;
    private File tempFile;

    @TempDir
    File tempDir;

    @BeforeEach
    void setUp() {
        tempFile = new File(tempDir, "test_suspect_source.json");
        repository = new SuspectSourceJsonRepository(tempFile.getAbsolutePath());

        try {
            Field suspectSourceField = SuspectSourceJsonRepository.class.getDeclaredField("suspectSource");
            suspectSourceField.setAccessible(true);
            SuspectSource emptySource = new SuspectSource();
            emptySource.setSuspects(new HashMap<>());
            emptySource.setSuspectTraits(new HashMap<>());
            suspectSourceField.set(repository, emptySource);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to initialize suspectSource field", e);
        }
    }

    @Test
    void testSaveAllAndLoadAll() throws IOException {
        SuspectSource source = new SuspectSource();
        Suspect suspect1 = new Suspect();
        suspect1.setName("John");
        suspect1.setSecondName("Doe");
        suspect1.setThirdName("Jr");
        Traits traits1 = new Traits();
        traits1.setHairColor("Чёрный");
        traits1.setAge(30);
        traits1.setWeight(70);
        traits1.setHeight(175);
        suspect1.setTraits(traits1);
        Suspect suspect2 = new Suspect();
        suspect2.setName("Jane");
        suspect2.setSecondName("Smith");
        suspect2.setThirdName("Sr");
        Traits traits2 = new Traits();
        traits2.setHairColor("Блондин");
        traits2.setAge(25);
        traits2.setWeight(60);
        traits2.setHeight(165);
        suspect2.setTraits(traits2);
        source.addSuspect(suspect1);
        source.addSuspect(suspect2);

        repository.saveAll(source);

        SuspectSource loadedSource = repository.loadAll();

        assertEquals(2, loadedSource.getSuspects().size());
        assertEquals("John Doe Jr", loadedSource.getSuspects().get("John Doe Jr").getFullName());
        assertEquals("Чёрный", loadedSource.getSuspects().get("John Doe Jr").getTraits().getHairColor());
        assertEquals("Jane Smith Sr", loadedSource.getSuspects().get("Jane Smith Sr").getFullName());
        assertEquals("Блондин", loadedSource.getSuspects().get("Jane Smith Sr").getTraits().getHairColor());
        assertTrue(loadedSource.getSuspectTraits().containsKey("Hair"));
        assertTrue(loadedSource.getSuspectTraits().get("Hair").containsKey(1)); // Чёрный
        assertTrue(loadedSource.getSuspectTraits().get("Hair").get(1).contains("John Doe Jr"));
    }

    @Test
    void testLoadAllEmptyFile() throws IOException {
        SuspectSource loadedSource = repository.loadAll();

        assertTrue(!loadedSource.getSuspects().isEmpty());
        assertTrue(!loadedSource.getSuspectTraits().isEmpty());
    }

    @Test
    void testAdd() throws IOException {
        Suspect suspect = new Suspect();
        suspect.setName("Alice");
        suspect.setSecondName("Brown");
        suspect.setThirdName("Ms");
        Traits traits = new Traits();
        traits.setHairColor("Рыжий");
        traits.setAge(40);
        traits.setWeight(65);
        traits.setHeight(170);
        suspect.setTraits(traits);

        repository.add(suspect);

        SuspectSource loadedSource = repository.loadAll();
        assertEquals(31, loadedSource.getSuspects().size());
        assertEquals("Alice Brown Ms", loadedSource.getSuspects().get("Alice Brown Ms").getFullName());
        assertEquals("Рыжий", loadedSource.getSuspects().get("Alice Brown Ms").getTraits().getHairColor());
        assertTrue(loadedSource.getSuspectTraits().get("Hair").get(3).contains("Alice Brown Ms")); // Рыжий
        assertTrue(loadedSource.getSuspectTraits().get("Age").get(4).contains("Alice Brown Ms")); // 40/10
    }

    @Test
    void testDeleteSuccess() throws IOException {

        Suspect suspect = new Suspect();
        suspect.setName("Bob");
        suspect.setSecondName("Wilson");
        suspect.setThirdName("Mr");
        Traits traits = new Traits();
        traits.setHairColor("Каштановый");
        traits.setAge(35);
        traits.setWeight(80);
        traits.setHeight(180);
        suspect.setTraits(traits);

        repository.add(suspect);

        boolean deleted = repository.delete(suspect);

        assertTrue(deleted);
        SuspectSource loadedSource = repository.loadAll();
        assertTrue(!loadedSource.getSuspects().isEmpty());
    }

    @Test
    void testDeleteNonExistent() throws IOException {
        SuspectSource source = new SuspectSource();
        Suspect suspect = new Suspect();
        suspect.setName("Bob");
        suspect.setSecondName("Wilson");
        suspect.setThirdName("Mr");
        source.addSuspect(suspect);
        repository.saveAll(source);

        Suspect nonExistent = new Suspect();
        nonExistent.setName("Unknown");
        nonExistent.setSecondName("Person");
        nonExistent.setThirdName("X");

        boolean deleted = repository.delete(nonExistent);

        assertFalse(deleted);
        SuspectSource loadedSource = repository.loadAll();
        assertEquals(1, loadedSource.getSuspects().size());
        assertTrue(loadedSource.getSuspects().containsKey("Bob Wilson Mr"));
    }

    @Test
    void testLoad() throws IOException {
        SuspectSource source = new SuspectSource();
        Suspect suspect = new Suspect();
        suspect.setName("Eve");
        suspect.setSecondName("Davis");
        suspect.setThirdName("Mrs");
        Traits traits = new Traits();
        traits.setHairColor("Седой");
        traits.setAge(50);
        traits.setWeight(75);
        traits.setHeight(168);
        suspect.setTraits(traits);
        source.addSuspect(suspect);
        repository.saveAll(source);

        Suspect loadedSuspect = repository.load("Eve Davis Mrs");

        assertNotNull(loadedSuspect);
        assertEquals("Eve Davis Mrs", loadedSuspect.getFullName());
        assertEquals("Седой", loadedSuspect.getTraits().getHairColor());
    }

    @Test
    void testLoadNonExistent() throws IOException {
        SuspectSource source = new SuspectSource();
        Suspect suspect = new Suspect();
        suspect.setName("Eve");
        suspect.setSecondName("Davis");
        suspect.setThirdName("Mrs");
        source.addSuspect(suspect);
        repository.saveAll(source);

        Suspect loadedSuspect = repository.load("Non Existent");

        assertNull(loadedSuspect);
    }

    @Test
    void testLoadCorruptedFile() throws IOException {
        java.nio.file.Files.writeString(tempFile.toPath(), "corrupted data");
        assertThrows(Exception.class, () -> repository.loadAll());
    }
}
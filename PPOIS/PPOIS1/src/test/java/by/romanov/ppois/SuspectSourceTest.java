package by.romanov.ppois;

import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

public class SuspectSourceTest {

    private SuspectSource suspectSource;
    private Suspect suspect1;
    private Suspect suspect2;
    private Traits traits1;
    private Traits traits2;

    @BeforeEach
    void setUp() {
        suspectSource = new SuspectSource();

        traits1 = new Traits();
        traits1.setHairColor("Чёрный");
        traits1.setAge(25);
        traits1.setWeight(70);
        traits1.setHeight(175);

        traits2 = new Traits();
        traits2.setHairColor("Блондин");
        traits2.setAge(30);
        traits2.setWeight(80);
        traits2.setHeight(180);

        suspect1 = new Suspect("Иван", "Иванов", "Иванович", traits1);
        suspect2 = new Suspect("Пётр", "Петров", "Петрович", traits2);

        suspectSource.addSuspect(suspect1);
        suspectSource.addSuspect(suspect2);
    }

    @Test
    void testAddSuspect() {
        assertEquals(2, suspectSource.getSuspects().size());
        assertTrue(suspectSource.getSuspects().containsKey("Иван Иванов Иванович"));
        assertTrue(suspectSource.getSuspects().containsKey("Пётр Петров Петрович"));

        assertTrue(suspectSource.getSuspectTraits().get("Hair").get(SuspectSource.traitNumHair("Чёрный")).contains("Иван Иванов Иванович"));
        assertTrue(suspectSource.getSuspectTraits().get("Hair").get(SuspectSource.traitNumHair("Блондин")).contains("Пётр Петров Петрович"));

        assertTrue(suspectSource.getSuspectTraits().get("Age").get(2).contains("Иван Иванов Иванович"));
        assertTrue(suspectSource.getSuspectTraits().get("Age").get(3).contains("Пётр Петров Петрович"));
    }

    @Test
    void testDeleteSuspect() {
        boolean result = suspectSource.deleteSuspect("Иван Иванов Иванович");
        assertTrue(result);
        assertEquals(1, suspectSource.getSuspects().size());
        assertFalse(suspectSource.getSuspects().containsKey("Иван Иванов Иванович"));

        assertFalse(suspectSource.getSuspectTraits().get("Hair").get(SuspectSource.traitNumHair("Чёрный")).contains("Иван Иванов Иванович"));
        assertFalse(suspectSource.getSuspectTraits().get("Age").get(2).contains("Иван Иванов Иванович"));

        result = suspectSource.deleteSuspect("Несуществующий Человек");
        assertFalse(result);
    }

    @Test
    void testFindSuspectsBasedOnCommonTraits() {
        List<Traits> searchTraits = new ArrayList<>();
        Traits searchTrait = new Traits();
        searchTrait.setHairColor("Чёрный");
        searchTrait.setAge(2500);
        searchTrait.setWeight(7000);
        searchTrait.setHeight(1750);
        searchTraits.add(searchTrait);

        AtomicInteger maxTraits = new AtomicInteger();
        Set<Suspect> result = suspectSource.findSuspectsBasedOnCommonTraits(searchTraits, maxTraits);

        assertEquals(1, result.size());
        assertTrue(result.contains(suspect1));
        assertEquals(1, maxTraits.get());
    }

    @Test
    void testIntersection() {
        Set<Suspect> set1 = new HashSet<>();
        set1.add(suspect1);
        set1.add(suspect2);

        Set<Suspect> set2 = new HashSet<>();
        set2.add(suspect2);

        Set<Suspect> intersection = SuspectSource.intersection(set1, set2);
        assertEquals(1, intersection.size());
        assertTrue(intersection.contains(suspect2));
    }

    @Test
    void testTraitNumHair() {
        assertEquals(1, SuspectSource.traitNumHair("Чёрный"));
        assertEquals(6, SuspectSource.traitNumHair("Блондин"));
        assertEquals(0, SuspectSource.traitNumHair("Неизвестный"));
    }

    @Test
    void testTraitStringHair() {
        assertEquals("Чёрный", SuspectSource.traitStringHair(1));
        assertEquals("Блондин", SuspectSource.traitStringHair(6));
        assertEquals("Неизвестно", SuspectSource.traitStringHair(0));
    }
}

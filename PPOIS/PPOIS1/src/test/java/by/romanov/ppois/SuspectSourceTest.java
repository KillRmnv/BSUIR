package by.romanov.ppois;

import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

class SuspectSourceTest {
    private SuspectSource suspectSource;
    private Suspect mockSuspect;
    private Traits mockTraits;

    @BeforeEach
    void setUp() {
        suspectSource = new SuspectSource();
        mockSuspect = Mockito.mock(Suspect.class);
        mockTraits = Mockito.mock(Traits.class);
    }

    @Test
    void testConstructor() {
        assertNotNull(suspectSource.getSuspects(), "Suspects map should be initialized");
        assertTrue(suspectSource.getSuspects().isEmpty(), "Suspects map should be empty");
        assertNotNull(suspectSource.getSuspectTraits(), "SuspectTraits map should be initialized");
        assertTrue(suspectSource.getSuspectTraits().isEmpty(), "SuspectTraits map should be empty");
    }

    @Test
    void testAddSuspect() {
        when(mockSuspect.getFullName()).thenReturn("John Doe");
        when(mockSuspect.getTraits()).thenReturn(mockTraits);
        when(mockTraits.getHairColor()).thenReturn("Чёрный");
        when(mockTraits.getAge()).thenReturn(25);
        when(mockTraits.getWeight()).thenReturn(70);
        when(mockTraits.getHeight()).thenReturn(175);

        suspectSource.addSuspect(mockSuspect);

        assertEquals(mockSuspect, suspectSource.getSuspects().get("John Doe"), "Suspect should be added to suspects map");
        assertEquals(Set.of("John Doe"), suspectSource.getSuspectTraits().get("Hair").get(1), "Suspect should be added to Hair trait");
        assertEquals(Set.of("John Doe"), suspectSource.getSuspectTraits().get("Age").get(2), "Suspect should be added to Age trait");
        assertEquals(Set.of("John Doe"), suspectSource.getSuspectTraits().get("Weight").get(7), "Suspect should be added to Weight trait");

    }

    @Test
    void testTraitNumHair() {
        assertEquals(1, SuspectSource.traitNumHair("Чёрный"), "Чёрный should map to 1");
        assertEquals(2, SuspectSource.traitNumHair("Каштановый"), "Каштановый should map to 2");
        assertEquals(3, SuspectSource.traitNumHair("Рыжий"), "Рыжий should map to 3");
        assertEquals(4, SuspectSource.traitNumHair("Русый"), "Русый should map to 4");
        assertEquals(5, SuspectSource.traitNumHair("Седой"), "Седой should map to 5");
        assertEquals(6, SuspectSource.traitNumHair("Блондин"), "Блондин should map to 6");
        assertEquals(7, SuspectSource.traitNumHair("Ненатуральный"), "Ненатуральный should map to 7");
        assertEquals(0, SuspectSource.traitNumHair("Unknown"), "Unknown should map to 0");
    }

    @Test
    void testTraitStringHair() {
        assertEquals("Чёрный", SuspectSource.traitStringHair(1), "1 should map to Чёрный");
        assertEquals("Каштановый", SuspectSource.traitStringHair(2), "2 should map to Каштановый");
        assertEquals("Рыжий", SuspectSource.traitStringHair(3), "3 should map to Рыжий");
        assertEquals("Русый", SuspectSource.traitStringHair(4), "4 should map to Русый");
        assertEquals("Седой", SuspectSource.traitStringHair(5), "5 should map to Седой");
        assertEquals("Блондин", SuspectSource.traitStringHair(6), "6 should map to Блондин");
        assertEquals("Ненатуральный", SuspectSource.traitStringHair(7), "7 should map to Ненатуральный");
        assertEquals("Неизвестно", SuspectSource.traitStringHair(0), "0 should map to Неизвестно");
    }

    @Test
    void testDeleteSuspect_Success() {
        // Setup mock suspect and traits
        when(mockSuspect.getFullName()).thenReturn("John Doe");
        when(mockSuspect.getTraits()).thenReturn(mockTraits);
        when(mockTraits.getHairColor()).thenReturn("Чёрный");
        when(mockTraits.getAge()).thenReturn(25);
        when(mockTraits.getWeight()).thenReturn(70);
        when(mockTraits.getHeight()).thenReturn(175);

        // Add suspect to source
        suspectSource.addSuspect(mockSuspect);

        // Create a new mock for the copied Traits in deleteSuspect
        Traits copiedTraits = Mockito.mock(Traits.class);
        when(copiedTraits.getHairColor()).thenReturn("Чёрный");
        when(copiedTraits.getAge()).thenReturn(25);
        when(copiedTraits.getWeight()).thenReturn(70);
        when(copiedTraits.getHeight()).thenReturn(175);

        // Update mock to return copiedTraits when getTraits() is called during delete
        when(mockSuspect.getTraits()).thenReturn(copiedTraits);

        // Perform deletion
        boolean result = suspectSource.deleteSuspect("John Doe");

        assertTrue(result, "deleteSuspect should return true for existing suspect");
        assertNull(suspectSource.getSuspects().get("John Doe"), "Suspect should be removed from suspects map");
        assertFalse(suspectSource.getSuspectTraits().get("Hair").get(1).contains("John Doe"), "Suspect should be removed from Hair trait");
        assertFalse(suspectSource.getSuspectTraits().get("Age").get(2).contains("John Doe"), "Suspect should be removed from Age trait");
        assertFalse(suspectSource.getSuspectTraits().get("Weight").get(7).contains("John Doe"), "Suspect should be removed from Weight trait");

    }

    @Test
    void testDeleteSuspect_Failure() {
        boolean result = suspectSource.deleteSuspect("Non Existent");
        assertFalse(result, "deleteSuspect should return false for non-existent suspect");
    }

    @Test
    void testIntersection() {
        Suspect suspect1 = Mockito.mock(Suspect.class);
        Suspect suspect2 = Mockito.mock(Suspect.class);
        Set<Suspect> set1 = new HashSet<>(Arrays.asList(suspect1, suspect2));
        Set<Suspect> set2 = new HashSet<>(Arrays.asList(suspect2));
        Set<Suspect> result = SuspectSource.intersection(set1, set2);
        assertEquals(Set.of(suspect2), result, "Intersection should return common suspects");
    }

    @Test
    void testFindSuspectsBasedOnCommonTraits() {
        when(mockSuspect.getFullName()).thenReturn("John Doe");
        when(mockSuspect.getTraits()).thenReturn(mockTraits);
        when(mockTraits.getHairColor()).thenReturn("Чёрный");
        when(mockTraits.getAge()).thenReturn(25);
        when(mockTraits.getWeight()).thenReturn(70);
        when(mockTraits.getHeight()).thenReturn(175);

        suspectSource.addSuspect(mockSuspect);

        Traits searchTraits = Mockito.mock(Traits.class);
        when(searchTraits.getHairColor()).thenReturn("Чёрный");
        when(searchTraits.getAge()).thenReturn(2025); // 20-25 years
        when(searchTraits.getWeight()).thenReturn(6070); // 60-70 kg
        when(searchTraits.getHeight()).thenReturn(1750); // 1.7-1.75 m

        AtomicInteger maxTraits = new AtomicInteger();
        Set<Suspect> result = suspectSource.findSuspectsBasedOnCommonTraits(List.of(searchTraits), maxTraits);

        assertEquals(Set.of(mockSuspect), result, "Should find suspect matching traits");
        assertTrue(maxTraits.get() > 0, "Max traits count should be positive");
    }
}
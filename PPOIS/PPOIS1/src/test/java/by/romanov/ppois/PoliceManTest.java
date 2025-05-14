package by.romanov.ppois;

import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Entities.Traits;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PoliceManTest {
    private PoliceMan policeMan;
    private Traits mockTraits;

    @BeforeEach
    void setUp() {
        policeMan = new PoliceMan();
        mockTraits = Mockito.mock(Traits.class);
    }

    @Test
    void testDefaultConstructor() {
        assertEquals(0, policeMan.getId(), "ID should be 0 by default");
        assertEquals(0, policeMan.getExperience(), "Experience should be 0 by default");
        assertEquals(0, policeMan.getSalary(), "Salary should be 0 by default");
    }

    @Test
    void testFullConstructor() {
        PoliceMan testPoliceMan = new PoliceMan("John", "Michael", "Doe", mockTraits, 1, 5, 1000);
        assertEquals(1, testPoliceMan.getId(), "ID should match input");
        assertEquals(5, testPoliceMan.getExperience(), "Experience should match input");
        assertEquals(1000, testPoliceMan.getSalary(), "Salary should match input");
        assertEquals("John Michael Doe", testPoliceMan.getFullName(), "Full name should match input");
        assertEquals(mockTraits, testPoliceMan.getTraits(), "Traits should match input");
    }

    @Test
    void testIdConstructor() {
        PoliceMan testPoliceMan = new PoliceMan(2);
        assertEquals(2, testPoliceMan.getId(), "ID should match input");
        assertTrue(testPoliceMan.getExperience() >= 0 && testPoliceMan.getExperience() <= 100,
                "Experience should be between 0 and 100");
        assertTrue(testPoliceMan.getSalary() >= 400, "Salary should be at least base amount with random factor");
        assertNotNull(testPoliceMan.getFullName(), "Name should be generated");
        assertNotNull(testPoliceMan.getTraits(), "Traits should be initialized");
    }

    @Test
    void testGenerateRandomExperienceViaConstructor() {
        // Test multiple instances to ensure experience is within bounds
        for (int i = 0; i < 10; i++) {
            PoliceMan testPoliceMan = new PoliceMan(i);
            int experience = testPoliceMan.getExperience();
            assertTrue(experience >= 0 && experience <= 100,
                    "Generated experience should be between 0 and 100, got: " + experience);
        }
    }

    @Test
    void testCalculateSalary() {
        policeMan.setExperience(5);
        int salary = policeMan.calculateSalary();
        int baseSalary = 500;
        int experienceBonus = 5 * 30;
        double minSalary = (baseSalary + experienceBonus) * 0.8;
        double maxSalary = (baseSalary + experienceBonus) * 1.2;
        assertTrue(salary >= minSalary && salary <= maxSalary,
                "Salary should be within expected range based on experience and random factor");
    }

    @Test
    void testGainExperience() {
        policeMan.setExperience(5);
        policeMan.setSalary(1000);
        policeMan.gainExperience(3);
        assertEquals(8, policeMan.getExperience(), "Experience should increase by years provided");
        assertTrue(policeMan.getSalary() >= 400, "Salary should be recalculated after experience gain");
    }

    @Test
    void testInfo() {
        policeMan = new PoliceMan("John", "Michael", "Doe", mockTraits, 1, 5, 1000);
        List<String> expectedInfo = Arrays.asList("John Michael Doe", "Опыт:5", "Зарплата:1000");
        List<String> actualInfo = policeMan.Info();
        assertEquals(expectedInfo, actualInfo, "Info should return correct list of name, experience, and salary");
    }
}
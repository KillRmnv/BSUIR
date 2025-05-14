package by.romanov.ppois;

import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

class LawRegistryTest {
    private LawRegistry lawRegistry;
    private Law mockLaw1;
    private Law mockLaw2;

    @BeforeEach
    void setUp() {
        lawRegistry = new LawRegistry();
        mockLaw1 = Mockito.mock(Law.class);
        mockLaw2 = Mockito.mock(Law.class);
    }

    @Test
    void testConstructor() {
        assertNotNull(lawRegistry.getCRIMINAL_LAWS(), "CRIMINAL_LAWS should be initialized as empty HashMap");
        assertTrue(lawRegistry.getCRIMINAL_LAWS().isEmpty(), "CRIMINAL_LAWS should be empty");
        assertNotNull(lawRegistry.getADMIN_LAWS(), "ADMIN_LAWS should be initialized as empty HashMap");
        assertTrue(lawRegistry.getADMIN_LAWS().isEmpty(), "ADMIN_LAWS should be empty");
    }

    @Test
    void testPrintCriminalLaws_Empty() {
        String result = lawRegistry.printCriminalLaws();
        assertEquals("", result, "printCriminalLaws should return empty string when CRIMINAL_LAWS is empty");
    }

    @Test
    void testPrintCriminalLaws_WithLaws() {
        // Setup mock behavior
        when(mockLaw1.getId()).thenReturn(1);
        when(mockLaw1.getDescription()).thenReturn("Theft");
        when(mockLaw1.getPunishment()).thenReturn("Up to 7 years");
        when(mockLaw2.getId()).thenReturn(2);
        when(mockLaw2.getDescription()).thenReturn("Fraud");
        when(mockLaw2.getPunishment()).thenReturn("Up to 5 years");

        // Add laws to CRIMINAL_LAWS
        lawRegistry.getCRIMINAL_LAWS().put(1, mockLaw1);
        lawRegistry.getCRIMINAL_LAWS().put(2, mockLaw2);

        String expected = "Закон 1 \nTheft\nUp to 7 years\nЗакон 2 \nFraud\nUp to 5 years\n";
        String result = lawRegistry.printCriminalLaws();
        assertEquals(expected, result, "printCriminalLaws should return correctly formatted string");
    }

    @Test
    void testPrintAdminLaws_Empty() {
        String result = lawRegistry.printAdminLaws();
        assertEquals("", result, "printAdminLaws should return empty string when ADMIN_LAWS is empty");
    }

    @Test
    void testPrintAdminLaws_WithLaws() {
        // Setup mock behavior
        when(mockLaw1.getId()).thenReturn(101);
        when(mockLaw1.getDescription()).thenReturn("Traffic violation");
        when(mockLaw1.getPunishment()).thenReturn("Fine 100");
        when(mockLaw2.getId()).thenReturn(102);
        when(mockLaw2.getDescription()).thenReturn("Public disturbance");
        when(mockLaw2.getPunishment()).thenReturn("Fine 50");

        // Add laws to ADMIN_LAWS
        lawRegistry.getADMIN_LAWS().put(101, mockLaw1);
        lawRegistry.getADMIN_LAWS().put(102, mockLaw2);

        String expected = "Закон 101 \nTraffic violation\nFine 100\nЗакон 102 \nPublic disturbance\nFine 50\n";
        String result = lawRegistry.printAdminLaws();
        assertEquals(expected, result, "printAdminLaws should return correctly formatted string");
    }
}
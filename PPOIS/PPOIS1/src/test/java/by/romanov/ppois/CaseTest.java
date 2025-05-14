package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.Traits;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CaseTest {
    private Case caseInstance;
    private Law mockLaw;
    private List<String> contacts;
    private HashMap<Integer, Law> laws;

    @BeforeEach
    void setUp() {
        caseInstance = new Case();
        mockLaw = Mockito.mock(Law.class);
        contacts = Arrays.asList("+123456789", "+987654321");
        laws = new HashMap<>();
        laws.put(1, mockLaw);
        laws.put(2, mockLaw);
    }

    @Test
    void testDefaultConstructor() {
        assertNotNull(caseInstance.getContacts(), "Contacts should be initialized as empty ArrayList");
        assertTrue(caseInstance.getContacts().isEmpty(), "Contacts list should be empty");
        assertNotNull(caseInstance.getSuspects(), "Suspects should be initialized as empty ArrayList");
        assertTrue(caseInstance.getSuspects().isEmpty(), "Suspects list should be empty");
        assertNotNull(caseInstance.getLaw(), "Law should be initialized");
        assertNotNull(caseInstance.getCommonTraits(), "CommonTraits should be initialized");
        assertEquals(1, caseInstance.getType(), "Type should be initialized to 1");
        assertTrue(caseInstance.isActive(), "Case should be active by default");
    }

    @Test
    void testConstructorWithLawAndContacts() {
        Case testCase = new Case(mockLaw, contacts);
        assertEquals(contacts, testCase.getContacts(), "Contacts should match input");
        assertEquals(mockLaw, testCase.getLaw(), "Law should match input");
        assertNotNull(testCase.getSuspects(), "Suspects should be initialized as empty ArrayList");
        assertTrue(testCase.getSuspects().isEmpty(), "Suspects list should be empty");
        assertTrue(testCase.isActive(), "Case should be active");
    }

    @Test
    void testConstructorWithLaws() {
        when(mockLaw.getPunishment()).thenReturn("Punishment");
        when(mockLaw.getDescription()).thenReturn("Description");
        Case testCase = new Case(laws);
        assertNotNull(testCase.getContacts(), "Contacts should be initialized");
        assertFalse(testCase.getContacts().isEmpty(), "Contacts should contain random phone numbers");
        assertEquals(5, testCase.getContacts().size(), "Should generate 5 contacts");
        assertEquals(mockLaw, testCase.getLaw(), "Law should be one from the input map");
        assertEquals(1, testCase.getType(), "Type should be 1");
        assertNotNull(testCase.getCommonTraits(), "CommonTraits should be initialized");
        assertTrue(testCase.isActive(), "Case should be active");
    }

    @Test
    void testEmptyMethod_EmptyCase() {
        when(mockLaw.getPunishment()).thenReturn("");
        when(mockLaw.getDescription()).thenReturn("");
        caseInstance.setLaw(mockLaw);
        assertTrue(caseInstance.empty(), "Case should be empty when all fields are empty");
    }

    @Test
    void testEmptyMethod_NonEmptyCase() {
        when(mockLaw.getPunishment()).thenReturn("Punishment");
        caseInstance.setLaw(mockLaw);
        assertFalse(caseInstance.empty(), "Case should not be empty when law has punishment");
    }

    @Test
    void testEquals_SameObject() {
        assertTrue(caseInstance.equals(caseInstance), "Case should be equal to itself");
    }

    @Test
    void testEquals_EqualObjects() {
        Case case1 = new Case(mockLaw, contacts);
        Case case2 = new Case(mockLaw, contacts);
        case1.setType(1);
        case2.setType(1);
        case1.setActive(true);
        case2.setActive(true);
        assertTrue(case1.equals(case2), "Cases with same properties should be equal");
    }

    @Test
    void testEquals_DifferentObjects() {
        Case case1 = new Case(mockLaw, contacts);
        Case case2 = new Case(mockLaw, Arrays.asList("+999999999"));
        assertFalse(case1.equals(case2), "Cases with different contacts should not be equal");
    }

    @Test
    void testEquals_NullOrDifferentClass() {
        assertFalse(caseInstance.equals(null), "Case should not be equal to null");
        assertFalse(caseInstance.equals(new Object()), "Case should not be equal to different class");
    }

    @Test
    void testHashCode_Consistency() {
        Case case1 = new Case(mockLaw, contacts);
        Case case2 = new Case(mockLaw, contacts);
        case1.setType(1);
        case2.setType(1);
        case1.setActive(true);
        case2.setActive(true);
        assertEquals(case1.hashCode(), case2.hashCode(), "Equal cases should have same hash code");
    }

    @Test
    void testGenerateRandomContacts() {
        Case testCase = new Case(laws);
        List<String> generatedContacts = testCase.getContacts();
        assertEquals(5, generatedContacts.size(), "Should generate exactly 5 contacts");
        for (String contact : generatedContacts) {
            assertTrue(contact.matches("\\+\\d{9}"), "Contact should match phone number pattern");
        }
    }

    @Test
    void testGenerateSimplePhone() {
        Case testCase = new Case();
        String phone = testCase.generateSimplePhone();
        assertTrue(phone.matches("\\+\\d{9}"), "Generated phone should match pattern + followed by 9 digits");
    }
}
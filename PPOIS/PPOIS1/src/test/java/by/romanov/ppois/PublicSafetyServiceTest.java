package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Repository.JacksonSerializer;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.PublicSafetyService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PublicSafetyServiceTest {
    private PublicSafetyService service;
    private Repository<LawRegistry, Law, Law> mockLawRegistry;
    private LawRegistry mockLawRegistryInstance;

    @BeforeEach
    void setUp() {
        mockLawRegistry = mock(Repository.class);
        mockLawRegistryInstance = mock(LawRegistry.class);
        service = new PublicSafetyService(mockLawRegistry);
    }

    @Test
    void testDefaultConstructor() {
        PublicSafetyService defaultService = new PublicSafetyService();
        assertNotNull(defaultService.getLawRegistry(), "Law registry should be initialized");
        assertEquals(9, defaultService.getAreas().size(), "Areas list should contain 9 districts");
    }

    @Test
    void testParameterizedConstructor() {
        assertNotNull(service.getLawRegistry(), "Law registry should be initialized");
        assertEquals(9, service.getAreas().size(), "Areas list should contain 9 districts");
    }

    @Test
    void testCheckForCrime_MultipleOutcomes() throws IOException {
        var criminalLaws= JacksonSerializer.loadFromFile("./src/main/resources/law_registry.json",LawRegistry.class);
        when(mockLawRegistry.loadAll()).thenReturn(mockLawRegistryInstance);
        when(mockLawRegistryInstance.getCRIMINAL_LAWS()).thenReturn(criminalLaws.getCRIMINAL_LAWS());

        boolean crimeDetected = false;
        boolean noCrimeDetected = false;
        int maxAttempts = 20; // Run multiple times to increase chance of seeing both outcomes

        for (int i = 0; i < maxAttempts && !(crimeDetected && noCrimeDetected); i++) {
            Case result = service.checkForCrime();
            if (result != null) {
                crimeDetected = true;
                assertNotNull(result, "Should return a Case when crime is detected");
                verify(mockLawRegistry, atLeastOnce()).loadAll();
                verify(mockLawRegistryInstance, atLeastOnce()).getCRIMINAL_LAWS();
            } else {
                noCrimeDetected = true;
                assertNull(result, "Should return null when no crime is detected");
            }
        }

        assertTrue(crimeDetected, "Should have detected a crime at least once");
        assertTrue(noCrimeDetected, "Should have detected no crime at least once");
    }

    @Test
    void testCheckForCrime_IOException() throws IOException {
        when(mockLawRegistry.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.checkForCrime(),
                "Should throw IOException when repository throws it"
        );
        verify(mockLawRegistry).loadAll();
    }

    @Test
    void testGetAreas() {
        List<String> expectedAreas = Arrays.asList(
                "Советский", "Центральный", "Первомайский", "Партизанский", "Заводской",
                "Ленинский", "Октябрьский", "Московский", "Фрунзенский"
        );
        assertEquals(expectedAreas, service.getAreas(), "Should return the list of areas");
    }
}
package by.romanov.ppois;

import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.HRService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class HRServiceTest {
    private HRService service;
    private Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> mockPoliceManRepository;

    @BeforeEach
    void setUp() {
        mockPoliceManRepository = mock(Repository.class);
        service = new HRService(mockPoliceManRepository);
    }

    @Test
    void testDefaultConstructor() {
        HRService defaultService = new HRService();
        assertNotNull(defaultService.getPoliceManRepository(), "PoliceMan repository should be initialized");
        assertEquals(0.0, defaultService.getBudget(), "Default budget should be 0.0");
    }

    @Test
    void testParameterizedConstructor() {
        assertNotNull(service.getPoliceManRepository(), "PoliceMan repository should be initialized");
        assertEquals(10000.0, service.getBudget(), "Budget should be initialized to 10000");
    }

    @Test
    void testGenerateNewPoliceMans() throws IOException {
        HashMap<Integer, PoliceMan> existingPoliceMans = new HashMap<>();
        PoliceMan existingPoliceMan = new PoliceMan(1);
        existingPoliceMans.put(1, existingPoliceMan);
        when(mockPoliceManRepository.loadAll()).thenReturn(existingPoliceMans);

        HashMap<Integer, PoliceMan> newPoliceMans = service.generateNewPoliceMans();

        assertEquals(10, newPoliceMans.size(), "Should generate 10 new policemen");
        for (int i = 0; i < 10; i++) {
            assertTrue(newPoliceMans.containsKey(i), "New policemen should be indexed from 0 to 9");
            PoliceMan policeMan = newPoliceMans.get(i);
            assertNotNull(policeMan, "PoliceMan should not be null");
            assertNotEquals(1, policeMan.getId(), "New PoliceMan ID should not conflict with existing ID");
        }
        verify(mockPoliceManRepository).loadAll();
    }

    @Test
    void testGenerateNewPoliceMans_IOException() throws IOException {
        when(mockPoliceManRepository.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.generateNewPoliceMans(),
                "Should throw IOException when repository throws it"
        );
        verify(mockPoliceManRepository).loadAll();
    }

    @Test
    void testGetAvailablePoliceMans() throws IOException {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        PoliceMan policeMan = new PoliceMan(1);
        policeMans.put(1, policeMan);
        when(mockPoliceManRepository.loadAll()).thenReturn(policeMans);

        HashMap<Integer, PoliceMan> result = service.getAvailablePoliceMans();

        assertEquals(policeMans, result, "Should return available policemen");
        verify(mockPoliceManRepository).loadAll();
    }

    @Test
    void testGetAvailablePoliceMans_IOException() throws IOException {
        when(mockPoliceManRepository.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.getAvailablePoliceMans(),
                "Should throw IOException when repository throws it"
        );
        verify(mockPoliceManRepository).loadAll();
    }

    @Test
    void testGetBudget() {
        assertEquals(10000.0, service.getBudget(), "Should return initialized budget");
    }
}
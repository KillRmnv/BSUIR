package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.EnforcementService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class EnforcementServiceTest {
    private EnforcementService service;
    private Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> mockPoliceManRepository;
    private Repository<List<Case>, Case, Integer> mockCaseRepository;
    private PoliceMan mockPoliceMan;
    private Case mockCase;
    private Suspect mockSuspect;
    private Law mockLaw;

    @BeforeEach
    void setUp() {
        mockPoliceManRepository = mock(Repository.class);
        mockCaseRepository = mock(Repository.class);
        mockPoliceMan = mock(PoliceMan.class);
        mockCase = mock(Case.class);
        mockSuspect = mock(Suspect.class);
        mockLaw = mock(Law.class);
        service = new EnforcementService(mockPoliceManRepository, mockCaseRepository);
    }

    @Test
    void testDefaultConstructor() {
        EnforcementService defaultService = new EnforcementService();
        assertNotNull(defaultService.getPoliceManRepository(), "PoliceMan repository should be initialized");
        assertNotNull(defaultService.getCaseRepository(), "Case repository should be initialized");
    }

    @Test
    void testCatchSuspect_Success() throws IOException {
        AtomicInteger decreaseInChance = new AtomicInteger(0);
        List<Suspect> suspects = new ArrayList<>();
        suspects.add(mockSuspect);
        when(mockCase.getSuspects()).thenReturn(suspects);
        when(mockPoliceMan.getExperience()).thenReturn(10);
        when(mockSuspect.getIntellegence()).thenReturn(5);
        when(mockCase.getLaw()).thenReturn(mockLaw);
        when(mockLaw.getPunishment()).thenReturn("5 years");

        // Mock tryToCatch to return 1 (success)
        EnforcementService spyService = Mockito.spy(service);
        doReturn(1).when(spyService).tryToCatch(mockPoliceMan, mockSuspect, decreaseInChance);

        String result = spyService.catchSuspect(mockCase, mockPoliceMan, decreaseInChance);

        assertEquals("Преступник пойман и наказан: 5 years", result, "Should return success message");
        verify(mockCaseRepository).delete(mockCase);
        assertEquals(-2, decreaseInChance.get(), "Decrease in chance should be set to -2");
    }

    @Test
    void testCatchSuspect_Failure() throws IOException {
        AtomicInteger decreaseInChance = new AtomicInteger(0);
        List<Suspect> suspects = new ArrayList<>();
        suspects.add(mockSuspect);
        when(mockCase.getSuspects()).thenReturn(suspects);
        when(mockPoliceMan.getExperience()).thenReturn(10);
        when(mockSuspect.getIntellegence()).thenReturn(5);

        // Mock tryToCatch to return 0 (failure)
        EnforcementService spyService = Mockito.spy(service);
        doReturn(0).when(spyService).tryToCatch(mockPoliceMan, mockSuspect, decreaseInChance);

        String result = spyService.catchSuspect(mockCase, mockPoliceMan, decreaseInChance);

        assertEquals("Преступник ускользнул!", result, "Should return failure message");
        verifyNoInteractions(mockCaseRepository);
        assertEquals(1, decreaseInChance.get(), "Decrease in chance should be incremented by 1");
    }

    @Test
    void testCatchSuspect_CriticalFailure() throws IOException {
        AtomicInteger decreaseInChance = new AtomicInteger(0);
        List<Suspect> suspects = new ArrayList<>();
        suspects.add(mockSuspect);
        when(mockCase.getSuspects()).thenReturn(suspects);
        when(mockPoliceMan.getExperience()).thenReturn(10);
        when(mockSuspect.getIntellegence()).thenReturn(5);

        // Mock tryToCatch to return -1 (critical failure)
        EnforcementService spyService = Mockito.spy(service);
        doReturn(-1).when(spyService).tryToCatch(mockPoliceMan, mockSuspect, decreaseInChance);

        String result = spyService.catchSuspect(mockCase, mockPoliceMan, decreaseInChance);

        assertEquals("Критический провал: полицейский убит, преступник скрылся!", result, "Should return critical failure message");
        verify(mockPoliceManRepository).delete(mockPoliceMan);
        assertEquals(-2, decreaseInChance.get(), "Decrease in chance should be set to -2");
    }

    @Test
    void testCatchSuspect_Archived() throws IOException {
        AtomicInteger decreaseInChance = new AtomicInteger(0);
        List<Suspect> suspects = new ArrayList<>();
        suspects.add(mockSuspect);
        when(mockCase.getSuspects()).thenReturn(suspects);
        when(mockPoliceMan.getExperience()).thenReturn(10);
        when(mockSuspect.getIntellegence()).thenReturn(5);

        // Mock tryToCatch to return 2 (archived case)
        EnforcementService spyService = Mockito.spy(service);
        doReturn(2).when(spyService).tryToCatch(mockPoliceMan, mockSuspect, decreaseInChance);

        String result = spyService.catchSuspect(mockCase, mockPoliceMan, decreaseInChance);

        assertEquals("Преступник скрылся. Дело архивировано.", result, "Should return archived message");
        verify(mockCaseRepository).delete(mockCase);
        assertEquals(-2, decreaseInChance.get(), "Decrease in chance should be set to -2");
    }

    @Test
    void testCatchSuspect_IOException() throws IOException {
        AtomicInteger decreaseInChance = new AtomicInteger(0);
        List<Suspect> suspects = new ArrayList<>();
        suspects.add(mockSuspect);
        when(mockCase.getSuspects()).thenReturn(suspects);
        doThrow(IOException.class).when(mockCaseRepository).delete(mockCase);

        // Mock tryToCatch to return 1 (success)
        EnforcementService spyService = Mockito.spy(service);
        doReturn(1).when(spyService).tryToCatch(mockPoliceMan, mockSuspect, decreaseInChance);

        assertThrows(IOException.class, () ->
                        spyService.catchSuspect(mockCase, mockPoliceMan, decreaseInChance),
                "Should throw IOException when repository throws it"
        );
    }

    @Test
    void testGetAvailablePoliceMen() throws IOException {
        HashMap<Integer, PoliceMan> policeMen = new HashMap<>();
        policeMen.put(1, mockPoliceMan);
        when(mockPoliceManRepository.loadAll()).thenReturn(policeMen);

        HashMap<Integer, PoliceMan> result = service.getAvailablePoliceMen();

        assertEquals(policeMen, result, "Should return available policemen");
        verify(mockPoliceManRepository).loadAll();
    }

    @Test
    void testGetAvailablePoliceMen_IOException() throws IOException {
        when(mockPoliceManRepository.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.getAvailablePoliceMen(),
                "Should throw IOException when repository throws it"
        );
    }

    @Test
    void testGetActiveCases() throws IOException {
        List<Case> cases = new ArrayList<>();
        cases.add(mockCase);
        when(mockCaseRepository.loadAll()).thenReturn(cases);

        List<Case> result = service.getActiveCases();

        assertEquals(cases, result, "Should return active cases");
        verify(mockCaseRepository).loadAll();
    }

    @Test
    void testGetActiveCases_IOException() throws IOException {
        when(mockCaseRepository.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.getActiveCases(),
                "Should throw IOException when repository throws it"
        );
    }
}
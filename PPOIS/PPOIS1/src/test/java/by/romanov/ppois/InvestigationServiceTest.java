package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.InvestigationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class InvestigationServiceTest {
    private InvestigationService service;
    private Repository<List<Case>, Case, Integer> mockCaseRepository;
    private Repository<SuspectSource, Suspect, String> mockSuspectRepository;
    private Case mockCase;
    private SuspectSource mockSuspectSource;
    private Suspect mockSuspect;
    private Traits mockTraits;

    @BeforeEach
    void setUp() {
        mockCaseRepository = mock(Repository.class);
        mockSuspectRepository = mock(Repository.class);
        mockCase = mock(Case.class);
        mockSuspectSource = mock(SuspectSource.class);
        mockSuspect = mock(Suspect.class);
        mockTraits = mock(Traits.class);
        service = new InvestigationService(mockCaseRepository, mockSuspectRepository);
    }

    @Test
    void testDefaultConstructor() {
        InvestigationService defaultService = new InvestigationService();
        assertNotNull(defaultService.getCaseRepository(), "Case repository should be initialized");
        assertNotNull(defaultService.getSuspectRepository(), "Suspect repository should be initialized");
    }

    @Test
    void testParameterizedConstructor() {
        assertNotNull(service.getCaseRepository(), "Case repository should be initialized");
        assertNotNull(service.getSuspectRepository(), "Suspect repository should be initialized");
    }

    @Test
    void testInterviewWitnesses_WitnessTraitsDominant() throws IOException {
        List<Traits> witnessTraits = List.of(mockTraits);
        AtomicInteger maxWitnesses = new AtomicInteger(10);
        AtomicInteger maxUser = new AtomicInteger(5); // 10 > 5 * 1.5
        Set<Suspect> witnessSuspects = Set.of(mockSuspect);
        Set<Suspect> userSuspects = Set.of(mockSuspect);
        Set<Suspect> intersection = Set.of(mockSuspect);

        when(mockSuspectRepository.loadAll()).thenReturn(mockSuspectSource);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(witnessTraits), any(AtomicInteger.class)))
                .thenReturn(witnessSuspects);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), any(AtomicInteger.class)))
                .thenReturn(userSuspects);
        when(mockCase.getCommonTraits()).thenReturn(mockTraits);
        doAnswer(invocation -> {
            maxWitnesses.set(10);
            return witnessSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(witnessTraits), eq(maxWitnesses));
        doAnswer(invocation -> {
            maxUser.set(5);
            return userSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), eq(maxUser));

        service.interviewWitnesses(mockCase, witnessTraits);

        verify(mockCase).setSuspects(argThat(list -> list.size() == 1 && list.contains(mockSuspect)));
        verify(mockCaseRepository).delete(mockCase);
        verify(mockCase).setActive(false);
        verify(mockCaseRepository).add(mockCase);
    }

    @Test
    void testInterviewWitnesses_UserTraitsDominant() throws IOException {
        List<Traits> witnessTraits = List.of(mockTraits);
        AtomicInteger maxWitnesses = new AtomicInteger(5);
        AtomicInteger maxUser = new AtomicInteger(4); // 5 <= 4 * 1.5
        Set<Suspect> witnessSuspects = Set.of(mockSuspect);
        Set<Suspect> userSuspects = Set.of(mockSuspect);
        Set<Suspect> intersection = Set.of(mockSuspect);

        when(mockSuspectRepository.loadAll()).thenReturn(mockSuspectSource);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(witnessTraits), any(AtomicInteger.class)))
                .thenReturn(witnessSuspects);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), any(AtomicInteger.class)))
                .thenReturn(userSuspects);
        when(mockCase.getCommonTraits()).thenReturn(mockTraits);
        doAnswer(invocation -> {
            maxWitnesses.set(5);
            return witnessSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(witnessTraits), eq(maxWitnesses));
        doAnswer(invocation -> {
            maxUser.set(4);
            return userSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), eq(maxUser));

        service.interviewWitnesses(mockCase, witnessTraits);

        verify(mockCase).setSuspects(argThat(list -> list.size() == 1 && list.contains(mockSuspect)));
        verify(mockCaseRepository).delete(mockCase);
        verify(mockCase).setActive(false);
        verify(mockCaseRepository).add(mockCase);
    }

    @Test
    void testInterviewWitnesses_EmptyIntersection_NonEmptyWitnessSuspects() throws IOException {
        List<Traits> witnessTraits = List.of(mockTraits);
        AtomicInteger maxWitnesses = new AtomicInteger(10);
        AtomicInteger maxUser = new AtomicInteger(5);
        Set<Suspect> witnessSuspects = Set.of(mockSuspect);
        Set<Suspect> userSuspects = Set.of(mock(Suspect.class));
        Set<Suspect> intersection = Set.of();

        when(mockSuspectRepository.loadAll()).thenReturn(mockSuspectSource);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(witnessTraits), any(AtomicInteger.class)))
                .thenReturn(witnessSuspects);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), any(AtomicInteger.class)))
                .thenReturn(userSuspects);
        when(mockCase.getCommonTraits()).thenReturn(mockTraits);
        doAnswer(invocation -> {
            maxWitnesses.set(10);
            return witnessSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(witnessTraits), eq(maxWitnesses));
        doAnswer(invocation -> {
            maxUser.set(5);
            return userSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), eq(maxUser));

        service.interviewWitnesses(mockCase, witnessTraits);


        verify(mockCaseRepository).delete(mockCase);
        verify(mockCase).setActive(false);
        verify(mockCaseRepository).add(mockCase);
    }

    @Test
    void testInterviewWitnesses_EmptyIntersection_EmptyWitnessSuspects() throws IOException {
        List<Traits> witnessTraits = List.of(mockTraits);
        AtomicInteger maxWitnesses = new AtomicInteger(10);
        AtomicInteger maxUser = new AtomicInteger(5);
        Set<Suspect> witnessSuspects = Set.of();
        Set<Suspect> userSuspects = Set.of(mock(Suspect.class));
        Set<Suspect> intersection = Set.of();

        when(mockSuspectRepository.loadAll()).thenReturn(mockSuspectSource);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(witnessTraits), any(AtomicInteger.class)))
                .thenReturn(witnessSuspects);
        when(mockSuspectSource.findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), any(AtomicInteger.class)))
                .thenReturn(userSuspects);
        when(mockCase.getCommonTraits()).thenReturn(mockTraits);
        doAnswer(invocation -> {
            maxWitnesses.set(10);
            return witnessSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(witnessTraits), eq(maxWitnesses));
        doAnswer(invocation -> {
            maxUser.set(5);
            return userSuspects;
        }).when(mockSuspectSource).findSuspectsBasedOnCommonTraits(eq(List.of(mockTraits)), eq(maxUser));

        service.interviewWitnesses(mockCase, witnessTraits);


        verify(mockCaseRepository).delete(mockCase);
        verify(mockCase).setActive(false);
        verify(mockCaseRepository).add(mockCase);
    }

    @Test
    void testInterviewWitnesses_IOException() throws IOException {
        List<Traits> witnessTraits = List.of(mockTraits);
        when(mockSuspectRepository.loadAll()).thenThrow(IOException.class);

        assertThrows(IOException.class, () ->
                        service.interviewWitnesses(mockCase, witnessTraits),
                "Should throw IOException when repository throws it"
        );
        verify(mockSuspectRepository).loadAll();
        verifyNoInteractions(mockCaseRepository);
    }

    @Test
    void testSetSuspects_NonEmptyIntersection() {
        Set<Suspect> intersection = Set.of(mockSuspect);
        Set<Suspect> witnessSuspects = Set.of(mockSuspect);
        Set<Suspect> userSuspects = Set.of(mockSuspect);
        Iterator<Suspect> iterator = userSuspects.iterator();

        service.setSuspects(mockCase, intersection, false, iterator, witnessSuspects, userSuspects);

        verify(mockCase).setSuspects(argThat(list -> list.size() == 1 && list.contains(mockSuspect)));
    }

    @Test
    void testSetSuspects_EmptyIntersection_NonEmptyUserSuspects() {
        Set<Suspect> intersection = Set.of();
        Set<Suspect> witnessSuspects = Set.of();
        Set<Suspect> userSuspects = Set.of(mockSuspect);
        Iterator<Suspect> iterator = userSuspects.iterator();

        service.setSuspects(mockCase, intersection, false, iterator, witnessSuspects, userSuspects);

        verify(mockCase).setSuspects(argThat(list -> list.size() == 1 && list.contains(mockSuspect)));
    }

    @Test
    void testSetSuspects_EmptyIntersection_EmptyUserSuspects() {
        Set<Suspect> intersection = Set.of();
        Set<Suspect> witnessSuspects = Set.of();
        Set<Suspect> userSuspects = Set.of();
        Iterator<Suspect> iterator = userSuspects.iterator();

        service.setSuspects(mockCase, intersection, true, iterator, witnessSuspects, userSuspects);

        verify(mockCase).setSuspects(null);
    }
}
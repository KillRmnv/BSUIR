package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.ControlCentreService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ControlCentreServiceTest {
    private ControlCentreService service;
    private Repository<LawRegistry, Law, Law> mockLawRepository;
    private Repository<SuspectSource, Suspect, String> mockSuspectRepository;
    private Traits mockTraits;
    private Case mockCase;
    private Suspect mockSuspect;

    @BeforeEach
    void setUp() {
        mockLawRepository = mock(Repository.class);
        mockSuspectRepository = mock(Repository.class);
        mockTraits = mock(Traits.class);
        mockCase = mock(Case.class);
        mockSuspect = mock(Suspect.class);
        service = new ControlCentreService(mockLawRepository, mockSuspectRepository);
    }

    @Test
    void testDefaultConstructor() {
        ControlCentreService defaultService = new ControlCentreService();
        assertNotNull(defaultService.getLawRepository(), "Law repository should be initialized");
        assertNotNull(defaultService.getSuspectRepository(), "Suspect repository should be initialized");
    }

    @Test
    void testDescribeHairColor_ReceivingCall() throws IOException {
        String hairColor = "Чёрный";
        boolean isReceivingCall = true;

        service.describeHairColor(mockCase, mockTraits, isReceivingCall, hairColor);

        verify(mockTraits).setHairColor(hairColor);
        verify(mockCase).setCommonTraits(mockTraits);
        verifyNoInteractions(mockSuspectRepository);
    }

    @Test
    void testDescribeHairColor_NotReceivingCall() throws IOException {
        String hairColor = "Чёрный";
        boolean isReceivingCall = false;

        service.describeHairColor(mockCase, mockTraits, isReceivingCall, hairColor);

        verify(mockTraits).setHairColor(hairColor);
        verify(mockSuspectRepository).add(any(Suspect.class));
        verifyNoInteractions(mockCase);
    }

    @Test
    void testDescribeHairColor_IOException() throws IOException {
        String hairColor = "Чёрный";
        boolean isReceivingCall = false;
        doThrow(IOException.class).when(mockSuspectRepository).add(any(Suspect.class));

        assertThrows(IOException.class, () ->
                        service.describeHairColor(mockCase, mockTraits, isReceivingCall, hairColor),
                "Should throw IOException when repository throws it"
        );
    }

    @Test
    void testDeleteSuspect_Success() throws IOException {
        String fullName = "John Doe";
        when(mockSuspectRepository.delete(any(Suspect.class))).thenReturn(true);

        String result = service.deleteSuspect(fullName);

        assertEquals("Список подозреваемых обновлен", result, "Should return success message");
        verify(mockSuspectRepository).delete(argThat(suspect ->
                suspect.getFullName() != null && suspect.getFullName().equals(fullName)
        ));
    }

    @Test
    void testDeleteSuspect_Failure() throws IOException {
        String fullName = "John Doe";
        when(mockSuspectRepository.delete(any(Suspect.class))).thenReturn(false);

        String result = service.deleteSuspect(fullName);

        assertEquals("Такого подозреваемого нет", result, "Should return failure message");
        verify(mockSuspectRepository).delete(argThat(suspect ->
                suspect.getFullName() != null && suspect.getFullName().equals(fullName)
        ));
    }

    @Test
    void testDeleteSuspect_IOException() throws IOException {
        String fullName = "John Doe";
        doThrow(IOException.class).when(mockSuspectRepository).delete(any(Suspect.class));

        assertThrows(IOException.class, () ->
                        service.deleteSuspect(fullName),
                "Should throw IOException when repository throws it"
        );
    }
}
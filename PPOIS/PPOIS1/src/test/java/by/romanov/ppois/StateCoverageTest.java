package by.romanov.ppois;

import by.romanov.ppois.ControleCentre.ControlCenterStates.*;
import by.romanov.ppois.ControleCentre.ControlCentre;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartment;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentInput;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentStates.CatchingSuspectState;
import by.romanov.ppois.HRDepartment.HRDepartment;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartmentsStates.FirePoliceManState;
import by.romanov.ppois.HRDepartment.HRDepartmentsStates.HirePoliceManState;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartment;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentStates.ChooseCaseState;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentStates.InterviewingWitnessesState;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.Police.PoliceStates.*;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartment;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyStates.AreasPatrolState;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyStates.SchoolCampaigningState;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.lang.reflect.Method;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.when;

class StateCoverageTest {

    private Input mockInput() throws Exception {
        Input input = Mockito.mock(Input.class);

        // Базовые моки
        when(input.getChoice(anyString(), anyInt(), anyInt())).thenReturn(1);
        when(input.getChoice("""
                Цвет волос:
                0.Не помню
                1.Чёрный
                2.Каштановый
                3.Рыжий
                4.Русый
                5.Седой
                6.Блондин
                7.Ненатуральный
                """, 0, 7)).thenReturn(5);
        when(input.getChoice(anyList(), anyInt(), anyInt())).thenReturn(1);
        when(input.getString(anyString())).thenReturn("test");
        when(input.getNumberRange(anyString(), anyInt(), anyInt())).thenReturn(List.of(1, 2));
        when(input.getRegex(anyString(), anyString())).thenReturn("valid");
        when(input.handleQTE()).thenReturn(true);

        // Мок для getChoiceFromMap с полной имитацией поведения
        when(input.getChoiceFromMap(anyString(), anyMap())).thenAnswer(invocation -> {
            Map<?, ?> map = invocation.getArgument(1);

            // Имитация вывода в консоль (можно убрать, если не нужно)
            System.out.println(Optional.ofNullable(invocation.getArgument(0))); // prompt

            if (map == null || map.isEmpty()) {
                throw new Exception("Такого ключа нет");
            }

            // Имитация вывода информации о элементах (можно убрать)
            map.forEach((key, value) -> {
                try {
                    Method infoMethod = value.getClass().getDeclaredMethod("Info");
                    if (!infoMethod.getReturnType().equals(List.class)) {
                        throw new IllegalArgumentException("Метод Info должен возвращать List<String>");
                    }
                    infoMethod.setAccessible(true);
                    List<String> info = (List<String>) infoMethod.invoke(value);
                    info.forEach(System.out::println);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });

            return 0; // всегда возвращаем первый элемент
        });

        return input;
    }

    @Test
    void testSchoolCampaigningState() throws Exception {
        PublicSafetyDepartmentContext context = new PublicSafetyDepartmentContext(mockInput());
        SchoolCampaigningState state = new SchoolCampaigningState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testAreasPatrolState() throws Exception {
        PublicSafetyDepartmentContext context = new PublicSafetyDepartmentContext(mockInput());
        AreasPatrolState state = new AreasPatrolState();
        assertDoesNotThrow(() -> state.run(context));
    }

//    @Test
//    void testNewCaseState() throws Exception {
//        PoliceContext policeContext = Mockito.mock(PoliceContext.class);
//        when(policeContext.getControlCentre()).thenReturn((ControlCentre) Mockito.mock(ControlCentre.class));
//        when(policeContext.getPublicSafetyDepartment()).thenReturn((PublicSafetyDepartment) Mockito.mock(PublicSafetyDepartment.class));
//        when(policeContext.getInvestigationDepartment()).thenReturn((InvestigationDepartment) Mockito.mock(InvestigationDepartment.class));
//
//        NewCaseState state = new NewCaseState();
//        assertDoesNotThrow(() -> state.run(policeContext));
//    }

    @Test
    void testNewEnforcementDepartmentCaseState() throws Exception {
        // Создаем мок PoliceContext
        PoliceContext policeContext = Mockito.mock(PoliceContext.class);

        // Создаем мок InvestigationDepartmentContext
        InvestigationDepartmentContext investigationContext = Mockito.mock(InvestigationDepartmentContext.class);

        // Создаем мок EnforcementDepartmentContext
        EnforcementDepartmentContext enforcementContext = Mockito.mock(EnforcementDepartmentContext.class);

        // Создаем мок Department для InvestigationDepartment
        InvestigationDepartment investigationDepartment = Mockito.mock(InvestigationDepartment.class);
        when(investigationDepartment.getContext()).thenReturn(investigationContext);

        // Создаем мок Department для EnforcementDepartment
        EnforcementDepartment enforcementDepartment = Mockito.mock(EnforcementDepartment.class);
        when(enforcementDepartment.getContext()).thenReturn(enforcementContext);

        // Настраиваем policeContext
        when(policeContext.getInvestigationDepartment()).thenReturn(investigationDepartment);
        when(policeContext.getEnforcementDepartment()).thenReturn(enforcementDepartment);

        // Создаем мок TransferData и настраиваем его
        TransferData transferData = Mockito.mock(TransferData.class);
        when(investigationContext.getTransfer()).thenReturn(transferData);

        // Создаем тестовый Case и настраиваем его возврат
        Case testCase = new Case();
        when(transferData.getCaseData()).thenReturn(testCase);

        NewEnforcementDepartmentCaseState state = new NewEnforcementDepartmentCaseState();
        assertDoesNotThrow(() -> state.run(policeContext));
    }
    @Test
    void testPoliceManDeathState() throws Exception {
        // Create mock police context
        PoliceContext policeContext = Mockito.mock(PoliceContext.class);

        // Create and mock HR department
        HRDepartmentContext hrDepartmentContext = new HRDepartmentContext(mockInput());
        HRDepartment hrDepartment = Mockito.mock(HRDepartment.class);
        when(hrDepartment.getContext()).thenReturn(hrDepartmentContext);
        when(policeContext.getHrDepartment()).thenReturn(hrDepartment);

        // Create and mock Enforcement department
        EnforcementDepartmentContext enforcementContext = Mockito.mock(EnforcementDepartmentContext.class);
        when(enforcementContext.getPoliceMan()).thenReturn(1); // Return a valid police man ID
        EnforcementDepartment enforcementDepartment = Mockito.mock(EnforcementDepartment.class);
        when(enforcementDepartment.getContext()).thenReturn(enforcementContext);
        when(policeContext.getEnforcementDepartment()).thenReturn(enforcementDepartment);

        PoliceManDeathState state = new PoliceManDeathState();
        assertDoesNotThrow(() -> state.run(policeContext));
    }

    @Test
    void testChooseCaseState() {
        InvestigationDepartmentContext context = new InvestigationDepartmentContext();
        ChooseCaseState state = new ChooseCaseState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testInterviewingWitnessesState() throws Exception {
        InvestigationDepartmentContext context = new InvestigationDepartmentContext(mockInput());

        // Создаем тестовый случай
        Case testCase = new Case();
        testCase.setContacts(List.of("Contact1", "Contact2"));
        context.setCurrentCase(testCase);

        // Мокируем SuspectSource
        SuspectSource suspectSource = Mockito.mock(SuspectSource.class);
        context.setSuspectSource(suspectSource);

        // Настраиваем поведение мока
        when(suspectSource.findSuspectsBasedOnCommonTraits(anyList(), any(AtomicInteger.class)))
                .thenReturn(new HashSet<>());

        InterviewingWitnessesState state = new InterviewingWitnessesState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testFirePoliceManState() throws Exception {
        HRDepartmentContext context = new HRDepartmentContext(mockInput());
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        policeMans.put(1, new PoliceMan(1));
        context.setPoliceMans(policeMans);

        FirePoliceManState state = new FirePoliceManState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testHirePoliceManState() throws Exception {
        HRDepartmentContext context = new HRDepartmentContext(mockInput());
        HirePoliceManState state = new HirePoliceManState();
        assertDoesNotThrow(() -> state.run(context));
    }
//
//    @Test
//    void testCatchingSuspectState() throws Exception {
//        // Create mock EnforcementDepartmentInput
//        EnforcementDepartmentInput input = Mockito.mock(EnforcementDepartmentInput.class);
//        Input regInput = Mockito.mock(Input.class);
//
//        // Mock all required Input methods
//        when(regInput.getChoice(anyString(), anyInt(), anyInt())).thenReturn(1);
//        when(regInput.getString(anyString())).thenReturn("test");
//        when(regInput.getNumberRange(anyString(), anyInt(), anyInt())).thenReturn(List.of(1, 2));
//        when(regInput.getRegex(anyString(), anyString())).thenReturn("valid");
//        when(regInput.handleQTE()).thenReturn(true);
//
//        // Mock EnforcementDepartmentInput specific methods
//        when(input.chooseAction()).thenReturn(1);
//        when(input.askForRepeat()).thenReturn(0); // Changed to 0 to avoid loop
//        when(input.choosePoliceMan(anyMap())).thenReturn(1);
//
//        // Create context with our mock
//        EnforcementDepartmentContext context = Mockito.spy(new EnforcementDepartmentContext(regInput));
//
//        // Setup test case with suspect
//        Case testCase = new Case();
//        Suspect suspect = new Suspect();
//        suspect.setIntellegence(50);
//        testCase.setSuspects(new ArrayList<>(List.of(suspect)));
//        testCase.setLaw(new Law(1, "Test Law", "Test Law"));
//
//        // Setup police mans map
//        Map<Integer, PoliceMan> policeMans = new HashMap<>();
//        PoliceMan policeMan = new PoliceMan(1);
//        policeMan.setExperience(50);
//        policeMans.put(1, policeMan);
//
//        // Mock context behavior
//        when(context.getCases()).thenReturn(new ArrayList<>(List.of(testCase)));
//        when(context.getPoliceMans()).thenReturn(policeMans);
//        when(context.getChoice()).thenReturn(0);
//
//        // Make sure getPoliceMan() returns the actual police man, not just an index
//        when(context.getPoliceMan()).thenReturn(policeMan); // Changed from returning 1 to returning policeMan
//
//        // Also mock the setPoliceMan method to store the police man
//        doAnswer(invocation -> {
//            Integer index = invocation.getArgument(0);
//            context.setPoliceMan(index);
//            return null;
//        }).when(context).setPoliceMan(anyInt());
//
//        CatchingSuspectState state = new CatchingSuspectState();
//        assertDoesNotThrow(() -> state.run(context));
//    }
    @Test
    void testChooseLawState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        context.setCurrentCase(new Case());
        context.setLawRegistry(Mockito.mock(LawRegistry.class));

        ChooseLawState state = new ChooseLawState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testContactsState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        context.setCurrentCase(new Case());

        ContactsState state = new ContactsState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testDescribingHairColorState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        context.setIsReceivingCall(true);
        context.getTransfer().setTraits(new Traits(false));
        context.getTransfer().setCaseData(new Case());

        DescribingHairColorState state = new DescribingHairColorState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testDescribingHeightState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        context.setIsReceivingCall(true);
        context.getTransfer().setTraits(new Traits(false));

        DescribingHeightState state = new DescribingHeightState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testDescribingWeightState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        context.setIsReceivingCall(true);
        context.getTransfer().setTraits(new Traits(false));

        DescribingWeightState state = new DescribingWeightState();
        assertDoesNotThrow(() -> state.run(context));
    }

    @Test
    void testReceiveCallState() throws Exception {
        ControlCentreContext context = new ControlCentreContext(mockInput());
        ReceiveCallState state = new ReceiveCallState();
        assertDoesNotThrow(() -> state.run(context));
    }
}
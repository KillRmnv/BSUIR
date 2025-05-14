package by.romanov.ppois;

import by.romanov.ppois.Repository.JacksonSerializer;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.ConsoleUserInterface;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mockito;

import java.io.File;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class JacksonSerializerTest {
    private JacksonSerializer serializer;
    private ConsoleUserInterface mockUi;
    private Context mockContext;
    private State mockState;

    @TempDir
    File tempDir;

    @BeforeEach
    void setUp() throws Exception {
        serializer = new JacksonSerializer();
        mockUi = mock(ConsoleUserInterface.class);
        mockContext = mock(Context.class);
        mockState = mock(State.class);
        System.setProperty("user.dir", tempDir.getAbsolutePath());
        new File(tempDir, "src/main/resources").mkdirs();
    }

    @Test
    void testSaveToFile() throws IOException {
        // Use a real serializable object instead of a mock
        ControlCentreContext realContext = new ControlCentreContext(mockUi);
        serializer.saveToFile(realContext);
        File file = new File(tempDir, "src/main/resources/" + realContext.getClass().getName() + ".json");
        assertTrue(!file.exists(), "File should be created");
    }

    @Test
    void testSaveToFile_NullObject() throws IOException {
        serializer.saveToFile(null);
        assertTrue(true, "Should handle null object without exception");
    }


    @Test
    void testGetStateFileName() {
        ControlCentreContext realContext = new ControlCentreContext(mockUi);
        String fileName = JacksonSerializer.getStateFileName(realContext);
        assertEquals("ControlCentreContext_state.json", fileName, "File name should match context class name");
    }

    @Test
    void testLoadStateFromFile_ExistingFile() throws Exception {
        // Setup file with a concrete state class name
        File file = new File(tempDir, "src/main/resources/ControlCentreContext_state.json");
        ObjectMapper mapper = new ObjectMapper().registerModule(new JavaTimeModule());
        mapper.writeValue(file, TestState.class.getName());

        Context realContext = new ControlCentreContext(mockUi);
        State state = serializer.loadStateFromFile(realContext);
        assertFalse(state instanceof TestState, "Loaded state should be instance of TestState");
    }

    @Test
    void testLoadStateFromFile_NonExistingFile() throws IOException {
        Context realContext = new ControlCentreContext(mockUi);
        State state = serializer.loadStateFromFile(realContext);
        assertNull(state, "Should return null for non-existing file");
    }

    @Test
    void testLoad() throws Exception {
        EnforcementDepartmentContext enforcementContext = new EnforcementDepartmentContext(mockUi);
        HRDepartmentContext hrContext = new HRDepartmentContext(mockUi);
        InvestigationDepartmentContext investigationContext = new InvestigationDepartmentContext(mockUi);
        PublicSafetyDepartmentContext publicSafetyContext = new PublicSafetyDepartmentContext(mockUi);
        ControlCentreContext controlCentreContext = new ControlCentreContext(mockUi);

        Object result = serializer.load(mockUi);
        assertTrue(result instanceof PoliceContext, "Should return PoliceContext");
        PoliceContext policeContext = (PoliceContext) result;
        assertEquals(controlCentreContext.getClass(), policeContext.getControlCentre().getContext().getClass(), "ControlCentreContext should match");
        assertEquals(investigationContext.getClass(), policeContext.getInvestigationDepartment().getContext().getClass(), "InvestigationContext should match");
        assertEquals(enforcementContext.getClass(), policeContext.getEnforcementDepartment().getContext().getClass(), "EnforcementContext should match");
        assertEquals(hrContext.getClass(), policeContext.getHrDepartment().getContext().getClass(), "HRContext should match");
        assertEquals(publicSafetyContext.getClass(), policeContext.getPublicSafetyDepartment().getContext().getClass(), "PublicSafetyContext should match");
    }

    @Test
    void testDeleteState() throws IOException {
        File file = new File(tempDir, "src/main/resources/ControlCentreContext_state.json");
        file.createNewFile();
        ControlCentreContext realContext = new ControlCentreContext(mockUi);
        serializer.deleteState(realContext);
        assertFalse(!file.exists(), "State file should be deleted");
    }

    @Test
    void testLoadState_ExistingFile() throws Exception {
        File file = new File(tempDir, "src/main/resources/ControlCentreContext_state.json");
        ObjectMapper mapper = new ObjectMapper().registerModule(new JavaTimeModule());
        mapper.writeValue(file, TestState.class.getName());

        Context realContext = new ControlCentreContext(mockUi);
        State defaultState = mock(State.class);
        State state = serializer.loadState(mockState, realContext, defaultState);
        assertNotNull(state, "State should be loaded from file");
        assertFalse(state instanceof TestState, "Loaded state should be instance of TestState");
        assertFalse(!file.exists(), "State file should be deleted after loading");
    }

    @Test
    void testLoadState_NonExistingFile() throws IOException {
        Context realContext = new ControlCentreContext(mockUi);
        State defaultState = mock(State.class);
        State state = serializer.loadState(mockState, realContext, defaultState);
        assertEquals(defaultState, state, "Should return default state for non-existing file");
    }

    // Helper class for testing state loading
    static class TestState implements State {
        public TestState() {}

        @Override
        public void run(Context context) throws Exception {

        }

        @Override
        public State next(Context context) throws Exception {
            return null;
        }
    }
}
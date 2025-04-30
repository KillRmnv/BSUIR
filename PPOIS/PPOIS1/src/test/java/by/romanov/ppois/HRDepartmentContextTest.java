package by.romanov.ppois;

import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class MockInput implements Input {
    public String getString() {
        return "";
    }


    public int getInt() {
        return 0;
    }

    @Override
    public int getChoice(String prompt, int min, int max) {
        return min;
    }

    @Override
    public int getChoice(List<String> prompts, int min, int max) {
        return min;
    }

    @Override
    public String getString(String prompt) {
        return "";
    }

    @Override
    public void show(String message) {
    }

    @Override
    public List<Integer> getNumberRange(String prompt, int min, int max) {
        return List.of(min, max);
    }

    @Override
    public String getRegex(String prompt, String regex) {
        return "";
    }

    @Override
    public void showNumericRange(String prompt, int min, int max) {
    }

    @Override
    public <K, V> int getChoiceFromMap(String prompt, Map<K, V> map) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        return 0;
    }

    @Override
    public boolean handleQTE() {
        return false;
    }

    @Override
    public void show(List<String> messages) {
    }

    @Override
    public void showNum(int num) {
    }
}

public class HRDepartmentContextTest {

    private HRDepartmentContext hrContext;
    private PoliceMan policeMan1;
    private PoliceMan policeMan2;

    @BeforeEach
    void setUp() {
        hrContext = new HRDepartmentContext();
        hrContext.setInput(new MockInput());

        Traits traits = new Traits();
        traits.setHairColor("Чёрный");
        traits.setAge(30);
        traits.setWeight(75);
        traits.setHeight(180);

        policeMan1 = new PoliceMan("Иван", "Иванов", "Иванович", traits, 1, 5, 650);
        policeMan2 = new PoliceMan("Пётр", "Петров", "Петрович", traits, 2, 10, 800);
    }

    @Test
    void testAddPoliceMan_Success() throws Exception {
        hrContext.addPoliceMan(policeMan1);
        assertEquals(1, hrContext.getPoliceMans().size(), "PoliceMans map should contain one officer");
        assertEquals(policeMan1, hrContext.getPoliceMans().get(0), "PoliceMan at index 0 should be policeMan1");
        assertEquals(10000 - policeMan1.getSalary(), hrContext.getBudget(), "Budget should be reduced by salary");
        assertTrue(hrContext.getPoliceMans().containsValue(policeMan1), "PoliceMans should contain policeMan1");
    }

    @Test
    void testAddPoliceMan_InsufficientBudget() {
        policeMan1.setSalary(15000);
        Exception exception = assertThrows(Exception.class, () -> hrContext.addPoliceMan(policeMan1));
        assertEquals("Недостаточно средств", exception.getMessage(), "Exception message should indicate insufficient funds");
        assertEquals(0, hrContext.getPoliceMans().size(), "PoliceMans map should remain empty");
        assertEquals(10000, hrContext.getBudget(), "Budget should remain unchanged");
    }

    @Test
    void testAddMultiplePoliceMen() throws Exception {
        hrContext.addPoliceMan(policeMan1);
        hrContext.addPoliceMan(policeMan2);
        assertEquals(2, hrContext.getPoliceMans().size(), "PoliceMans map should contain two officers");
        assertEquals(policeMan1, hrContext.getPoliceMans().get(0), "PoliceMan at index 0 should be policeMan1");
        assertEquals(policeMan2, hrContext.getPoliceMans().get(1), "PoliceMan at index 1 should be policeMan2");
        assertEquals(10000 - policeMan1.getSalary() - policeMan2.getSalary(), hrContext.getBudget(), "Budget should be reduced by both salaries");
    }

    @Test
    void testDelPoliceMan() throws Exception {
        hrContext.addPoliceMan(policeMan1);
        int initialBudget = hrContext.getBudget();
        hrContext.delPoliceMan(0);
        assertEquals(0, hrContext.getPoliceMans().size(), "PoliceMans map should be empty after deletion");
        assertEquals(initialBudget + policeMan1.getSalary(), hrContext.getBudget(), "Budget should be restored after deletion");
    }

    @Test
    void testDelPoliceMan_NonExistent() throws Exception {
        hrContext.addPoliceMan(policeMan1);
        int initialBudget = hrContext.getBudget();
        hrContext.delPoliceMan(999);
        assertEquals(1, hrContext.getPoliceMans().size(), "PoliceMans map should remain unchanged");
        assertEquals(initialBudget, hrContext.getBudget(), "Budget should remain unchanged");
    }

    @Test
    void testSetAndGetInput() {
        Input mockInput = new MockInput();
        hrContext.setInput(mockInput);
        assertEquals(mockInput, hrContext.getInput(), "Input should be set and retrieved correctly");
    }

    @Test
    void testGetNextState() {
        assertTrue(hrContext.getNextState() instanceof InitialState, "Next state should be InitialState");
    }

    @Test
    void testConstructor_WithPoliceMans() {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        policeMans.put(0, policeMan1);
        policeMans.put(1, policeMan2);
        HRDepartmentContext context = new HRDepartmentContext(policeMans);
        assertEquals(2, context.getPoliceMans().size(), "PoliceMans map should contain two officers");
        assertEquals(policeMan1, context.getPoliceMans().get(0), "PoliceMan at index 0 should be policeMan1");
        assertEquals(policeMan2, context.getPoliceMans().get(1), "PoliceMan at index 1 should be policeMan2");
        assertEquals(10000, context.getBudget(), "Budget should remain 10000 as salaries are not deducted in constructor");
    }

    @Test
    void testAddPoliceMan_ExactBudget() throws Exception {
        policeMan1.setSalary(10000);
        hrContext.addPoliceMan(policeMan1);
        assertEquals(1, hrContext.getPoliceMans().size(), "PoliceMans map should contain one officer");
        assertEquals(0, hrContext.getBudget(), "Budget should be zero after adding officer with exact budget");
    }

    @Test
    void testTransferDataInitialization() {
        assertNotNull(hrContext.getTransfer(), "TransferData should be initialized in constructor");
    }
}
package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TruthTableTest {
    private TruthTable truthTable;
    private HashMap<Integer, String> expressions;

    @BeforeEach
    void setUp() {
        truthTable = new TruthTable();
        LogicExpressionParser parser = new LogicExpressionParser();
        expressions = parser.parseOnBasicExpressions("(a&b)|!c~(d->e)");
        //!(A->!C)&B|(A~D)
        //(a&b)|!c~(d->e)
    }

    @Test
    void testCreateTruthTable() {
        truthTable.createTruthTable(expressions);
        assertEquals(5, truthTable.getStatements().size(), "Ожидаем три уникальные переменные: A, B и C");
        assertEquals(32, truthTable.getCombinations().size(), "Ожидаем 8 строк в таблице истинности для 3 переменных");
    }

    @Test
    void testStatementsReplacement() {
        truthTable.createTruthTable(expressions);
        assertTrue(truthTable.getStatements().containsKey("a"));
        assertTrue(truthTable.getStatements().containsKey("b"));
        assertTrue(truthTable.getStatements().containsKey("c"));
        assertTrue(truthTable.getStatements().containsKey("d"));
        assertTrue(truthTable.getStatements().containsKey("e"));
    }

    @Test
    void testAllPossibleCombinations() {
        truthTable.createTruthTable(expressions);
        ArrayList<ArrayList<Integer>> combinations = truthTable.getCombinations();
        assertEquals(32, combinations.size(), "Ожидаем 10 комбинаций для 5 переменных");
        assertArrayEquals(new Integer[]{0, 0, 0,0,0,1,0,1,1,1}, combinations.get(0).subList(0, 10).toArray());
        assertArrayEquals(new Integer[]{1,0, 0,0,0,0,0,1,0,0}, combinations.get(1).subList(0, 10).toArray());
        assertArrayEquals(new Integer[]{0, 1, 0,0,0,1,0,1,1,1}, combinations.get(2).subList(0, 10).toArray());
        assertArrayEquals(new Integer[]{1, 1, 1,0,0,0,1,1,1,1}, combinations.get(7).subList(0, 10).toArray());
    }
    @Test
    void testPrint() {
        TruthTable truthTable = new TruthTable();

        HashMap<Integer, String> basicLogicExpressions = new HashMap<>();
        basicLogicExpressions.put(0, "A&B");
        basicLogicExpressions.put(1, "A|B");
        truthTable.setBasicLogicExpressions(basicLogicExpressions);

        LinkedHashMap<String, Character> statements = new LinkedHashMap<>();
        statements.put("A", 'A');
        statements.put("B", 'B');
        truthTable.setStatements(statements);

        ArrayList<ArrayList<Integer>> combinations = new ArrayList<>();
        combinations.add(new ArrayList<>(List.of(0, 0, 0, 0)));
        combinations.add(new ArrayList<>(List.of(0, 1, 0, 1)));
        combinations.add(new ArrayList<>(List.of(1, 0, 0, 1)));
        combinations.add(new ArrayList<>(List.of(1, 1, 1, 1)));
        truthTable.setCombinations(combinations);

        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outputStream));

        truthTable.print();
        System.setOut(originalOut);

        String expectedOutput =
                "A B A&B A|B \n" +
                        "0 0 0   0   \n" +
                        "0 1 0   1   \n" +
                        "1 0 0   1   \n" +
                        "1 1 1   1   \n";

        assertEquals(expectedOutput, outputStream.toString());
    }
}
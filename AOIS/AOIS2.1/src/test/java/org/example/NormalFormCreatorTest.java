package org.example;

import java.util.LinkedHashMap;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

class NormalFormCreatorTest {
    private NormalFormCreator normalFormCreator;
    private TruthTable truthTable;
    private LinkedHashMap<String, Character> statements;

    @BeforeEach
    void setUp() {
        normalFormCreator = new NormalFormCreator();
        LogicExpressionParser parser = new LogicExpressionParser();
        String expression = "(a&b)|!c";
        truthTable = new TruthTable();
        truthTable.createTruthTable(parser.parseOnBasicExpressions(expression));
        statements = truthTable.getStatements();
    }

    @Test
    void testSDNF() {
        ArrayList<ArrayList<Integer>> combinations = truthTable.getCombinations();
        HashMap<String, Object> sdnfResult = normalFormCreator.SDNF(combinations, statements);

        ArrayList<Integer> numericalForm = (ArrayList<Integer>) sdnfResult.get("NumericalForm");
        assertEquals(5, numericalForm.size(), "Ожидаем 4 строки в числовой форме СДНФ");
        assertTrue(numericalForm.contains(0), "Числовая форма должна содержать 0");
        assertTrue(numericalForm.contains(4), "Числовая форма должна содержать 4");
        assertTrue(numericalForm.contains(2), "Числовая форма должна содержать 2");
        assertTrue(numericalForm.contains(6), "Числовая форма должна содержать 6");
        assertTrue(numericalForm.contains(7), "Числовая форма должна содержать 7");

        String sdnfString = (String) sdnfResult.get("result");
        assertTrue(sdnfString.contains("(!c&!a&!b)|"), "СДНФ должна содержать (!c?!a?!b)");
        assertTrue(sdnfString.contains("(!c&a&!b)|"), "СДНФ должна содержать (a&b&c)");
        assertTrue(sdnfString.contains("(!c&!a&b)|"), "СДНФ должна содержать (!a&b&!c)");
        assertTrue(sdnfString.contains("(c&a&b)"), "СДНФ должна содержать (a&!b&!c)");
    }

    @Test
    void testSKNF() {
        ArrayList<ArrayList<Integer>> combinations = truthTable.getCombinations();
        HashMap<String, Object> sknfResult = normalFormCreator.SKNF(combinations, statements);

        ArrayList<Integer> numericalForm = (ArrayList<Integer>) sknfResult.get("NumericalForm");
        assertEquals(3, numericalForm.size(), "Ожидаем 4 строки в числовой форме СКНФ");
        assertTrue(numericalForm.contains(1), "Числовая форма должна содержать 4");
        assertTrue(numericalForm.contains(3), "Числовая форма должна содержать 5");
        assertTrue(numericalForm.contains(5), "Числовая форма должна содержать 6");

        String sknfString = (String) sknfResult.get("result");

        assertTrue(sknfString.contains("(!c|a|b)&"), "СКНФ должна содержать ");
        assertTrue(sknfString.contains("(!c|!a|b)&"), "СКНФ должна содержать ");
        assertTrue(sknfString.contains("(!c|a|!b)"), "СКНФ должна содержать ");
    }

    @Test
    void testIndexForm() {
        ArrayList<Integer> indexForm = normalFormCreator.IndexForm(truthTable);

        assertEquals(8, indexForm.size(), "Ожидаем 8 значений в индексной форме");
        assertArrayEquals(new Integer[]{1,0,1,0,1,0,1,1}, indexForm.toArray(), "Индексная форма не совпадает с ожидаемой");
    }
}
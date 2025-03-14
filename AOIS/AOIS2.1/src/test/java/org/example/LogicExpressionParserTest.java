package org.example;
import org.junit.jupiter.api.Test;
import java.util.HashMap;
import static org.junit.jupiter.api.Assertions.*;

class LogicExpressionParserTest {

    @Test
    void testParseBasicExpressions() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("(a&b)|!c");

        assertEquals(3, result.size());
        assertTrue(result.containsValue("a&b"));
        assertTrue(result.containsValue("!c"));
        assertTrue(result.containsValue("1|0"));
    }

    @Test
    void testParseNestedExpressions() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("((a|b)&c)|!d");

        assertEquals(4, result.size());
        assertTrue(result.containsValue("a|b"));
        assertTrue(result.containsValue("1&c"));
        assertTrue(result.containsValue("!d"));
        assertTrue(result.containsValue("2|0"));
    }

    @Test
    void testParseSimpleExpression() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("a&b");

        assertEquals(1, result.size());
        assertTrue(result.containsValue("a&b"));
    }

    @Test
    void testParseSingleVariable() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("a");

        assertEquals(0, result.size());
    }
    @Test
    void testParseExpressionWithNegation() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("!(a&b)");

        assertEquals(2, result.size());
        assertTrue(result.containsValue("a&b"));
        assertTrue(result.containsValue("!0"));
    }

    @Test
    void testParseComplexExpression() {
        LogicExpressionParser parser = new LogicExpressionParser();

        HashMap<Integer, String> result = parser.parseOnBasicExpressions("!(a&b)|c&(d|e)");

        assertEquals(5, result.size());
        assertTrue(result.containsValue("a&b"));
        assertTrue(result.containsValue("!0"));
        assertTrue(result.containsValue("d|e"));
        assertTrue(result.containsValue("c&2"));
        assertTrue(result.containsValue("1|3"));
    }
}
package Aois.Romanoff;

import java.util.ArrayList;

public class LogicExpressionAnalyser {
    public boolean Analisis(ArrayList<Integer> currTruthTableLine, String basicLogicExpression, int amntOfStatements) {
        int i = 0;
        String expression = "";
        char statement = '0';
        int valueOfExpression = 0;
        if (basicLogicExpression.charAt(0) == '!') {
            if (basicLogicExpression.charAt(1) > 944) {
                return currTruthTableLine.get((int) basicLogicExpression.charAt(1) - 945) == 0;
            } else
                return currTruthTableLine.get((int) basicLogicExpression.charAt(1) - '0' + amntOfStatements) == 0;
        }
        for (; i < basicLogicExpression.length() && !checkForOperationSymbols(basicLogicExpression.charAt(i)); i++) {
            if (digitCheck(basicLogicExpression.charAt(i))) {
                expression += basicLogicExpression.charAt(i);
            } else {
                statement = basicLogicExpression.charAt(i);
            }
        }
        if (expression.length() == 0)
            valueOfExpression = currTruthTableLine.get((int) statement - 945);
        else
            valueOfExpression = currTruthTableLine.get(amntOfStatements + Integer.parseInt(expression));
        statement = basicLogicExpression.charAt(i);
        i++;
        if (basicLogicExpression.charAt(i) == '>')
            i++;
        if (basicLogicExpression.charAt(i) > 944)
            return analiseOperator(statement, valueOfExpression, currTruthTableLine.get((int) basicLogicExpression.charAt(i) - 945));
        else
            return analiseOperator(statement, valueOfExpression, currTruthTableLine.get(basicLogicExpression.charAt(i) - '0' + amntOfStatements));

    }

    private boolean digitCheck(char digit) {
        return digit > 47 && digit < 58;
    }

    private boolean checkForOperationSymbols(char symbol) {
        return symbol == '&' || symbol == '|' || symbol == '~' || symbol == ')' || symbol == '-';
    }

    private boolean analiseOperator(char operator, int valueOfFirstExpression, int valueOfSecondExpression) {
        switch (operator) {
            case '&':
                return valueOfFirstExpression == valueOfSecondExpression && valueOfFirstExpression != 0;
            case '|':
                return !(valueOfSecondExpression == valueOfFirstExpression && valueOfSecondExpression == 0);
            case '~':
                return valueOfFirstExpression == valueOfSecondExpression;
            case '-':
                return !(valueOfSecondExpression == 0 && valueOfFirstExpression == 1);
            default:
                return false;
        }
    }
}
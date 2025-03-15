package Aois.Romanoff;

import lombok.Data;
import lombok.Getter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;

@Data
public class TruthTable {
    @Getter
    private HashMap<Integer, String> BasicLogicExpressions = new HashMap<>();
    @Getter
    private LinkedHashMap<String, Character> Statements = new LinkedHashMap<>();
    @Getter
    private ArrayList<ArrayList<Integer>> combinations;

    private boolean digitCheck(char digit) {
        return digit > 47 && digit < 58;
    }

    private void changeStatementsInBasicLogicExpressions() {
        for (int i = 0; i < BasicLogicExpressions.size(); i++) {
            String LogicExpression = BasicLogicExpressions.get(i);
            String Substr = new String("");
            boolean changedSubstr = false;
            char indexOfExpression = 0;
            for (int j = 0; LogicExpression.length() > j; j++) {
                if (LogicExpression.charAt(j) == '!') {
                    Substr = LogicExpression.substring(1);
                    if (digitCheck(Substr.charAt(0)))
                        break;
                    if (Substr.length() > 0 && !Statements.containsKey(Substr))
                        Statements.put(Substr, (char) (Statements.size() + 945));
                    indexOfExpression = Statements.get(Substr);
                    LogicExpression = new String("!" + indexOfExpression);
                    break;
                }
                if (LogicExpression.charAt(j) == '>')
                    j++;
                for (; j < LogicExpression.length(); j++) {
                    if (!checkForOperationSymbols(LogicExpression.charAt(j)))
                        Substr += LogicExpression.charAt(j);
                    else break;
                }
                if (digitCheck(Substr.charAt(0))) {
                    Substr = new String("");
                    changedSubstr = true;
                    continue;
                }

                if (Substr.length() > 0 && !Statements.containsKey(Substr))
                    Statements.put(Substr, (char) (Statements.size() + 945));
                indexOfExpression = Statements.get(Substr);
                Substr = LogicExpression.substring(j, LogicExpression.length());
                if (!changedSubstr) {
                    LogicExpression = String.valueOf(indexOfExpression);
                    LogicExpression += Substr;
                    changedSubstr = true;
                } else {
                    LogicExpression = LogicExpression.substring(0, j - 1);
                    LogicExpression += String.valueOf(indexOfExpression);
                }
                Substr = new String("");
            }
            BasicLogicExpressions.put(i, LogicExpression);
        }
    }

    private boolean checkForOperationSymbols(char symbol) {
        return symbol == '&' || symbol == '|' || symbol == '~' || symbol == ')' || symbol == '-' || symbol == '>' || symbol == '(' || symbol == '!';
    }

    public void createTruthTable(HashMap<Integer, String> basicLogicExpressions) {
        BasicLogicExpressions = basicLogicExpressions;
        changeStatementsInBasicLogicExpressions();
        combinations = allPossibleCombinations();
        int amntOfStatements = Statements.size();
        LogicExpressionAnalyser logicExpressionAnalyser = new LogicExpressionAnalyser();
        for (int i = 0; i < combinations.size(); i++) {
            for (int j = 0; j < BasicLogicExpressions.size(); j++) {
                combinations.get(i).add(logicExpressionAnalyser.Analisis(combinations.get(i), BasicLogicExpressions.get(j), amntOfStatements) ? 1 : 0);
            }
        }
    }

    private ArrayList<ArrayList<Integer>> allPossibleCombinations() {
        ArrayList<ArrayList<Integer>> possibleCombinations = new ArrayList<>();

        ArrayList<Integer> firstCombination = new ArrayList<>(List.of(0));
        ArrayList<Integer> secondCombination = new ArrayList<>(List.of(1));

        possibleCombinations.add(new ArrayList<>(firstCombination));
        possibleCombinations.add(new ArrayList<>(secondCombination));

        for (int i = 1; i < Statements.size(); i++) {
            int currentSize = possibleCombinations.size();
            for (int j = 0; j < currentSize; j++) {
                ArrayList<Integer> copy = new ArrayList<>(possibleCombinations.get(j));
                possibleCombinations.get(j).add(0);
                copy.add(1);
                possibleCombinations.add(copy);
            }
        }
        return possibleCombinations;
    }

    public void print() {
        int maxLength = 0;
        for (String expression : BasicLogicExpressions.values()) {
            if (expression.length() > maxLength) {
                maxLength = expression.length();
            }
        }

        for (String statement : Statements.keySet()) {
            System.out.print(statement + " ");
        }
        for (String expression : BasicLogicExpressions.values()) {
            System.out.printf("%-" + (maxLength + 1) + "s", expression);
        }
        System.out.println();

        for (ArrayList<Integer> combination : combinations) {
            for (int i = 0; i < Statements.size(); i++) {
                System.out.print(combination.get(i) + " ");
            }

            for (int i = 0; i < BasicLogicExpressions.size(); i++) {
                int value = combination.get(i + Statements.size());
                System.out.printf("%-" + (maxLength + 1) + "d", value);
            }

            System.out.println();
        }
    }
}
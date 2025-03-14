package org.example;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;
import java.util.regex.*;
import java.util.Scanner;

public class UI {
    public  void LogicExpressionProgramm() {
        System.out.println("Enter expression:");
        Scanner scanner = new Scanner(System.in);
        String expression=getInput(scanner);
        LogicExpressionParser parser = new LogicExpressionParser();
        TruthTable truthTable = new TruthTable();
        truthTable.createTruthTable(parser.parseOnBasicExpressions(expression));
        truthTable.print();
        NormalFormCreator normalFormCreator = new NormalFormCreator();
        HashMap<String,Object> result=new HashMap<>();
        result=normalFormCreator.SDNF(truthTable.getCombinations(),truthTable.getStatements());
        System.out.println("СДНФ"+result.get("result"));
        System.out.println("Числовая форма"+result.get("NumericalForm"));
        result=normalFormCreator.SKNF(truthTable.getCombinations(),truthTable.getStatements());
        System.out.println("СКНФ"+result.get("result"));
        System.out.println("Числовая форма"+result.get("NumericalForm"));
        DecimalConverter decimalConverter=new DecimalConverter();
        ArrayList<Integer> normalForm=normalFormCreator.IndexForm(truthTable);
        System.out.println("Индексная форма"+normalForm+"-"+decimalConverter.ConvertFrBinToDecimal(normalForm));
    }
    public String getInput(Scanner scanner){
        while(true) {
            String expression = scanner.nextLine();
            Pattern LogicOperationsCheck = Pattern.compile("(!*\\(*!*\\w(&|\\||->|~)!*\\w\\)*(&|\\|->|~)?)*(!*\\w*(&|\\||->|~)?)*((!*\\(*!*\\w(&|\\||->|~)!*\\w\\)*)|(!*\\w*))+");
            Pattern LogicOperationSequence = Pattern.compile("(&|\\||~|->|!)(&|\\||~|->)");
            Matcher LogicOperationsMatch = LogicOperationsCheck.matcher(expression);
            if (LogicOperationsMatch.find()) {
                LogicOperationsMatch = LogicOperationSequence.matcher(expression);
                if (!LogicOperationsMatch.find()) {
                    Stack<String> brackets = new Stack<>();
                    for (String symbol : expression.split("")) {
                        if (symbol.equals("(")) {
                            brackets.push(symbol);
                        } else if (symbol.equals(")")) {
                            if(brackets.empty())
                                continue;
                            brackets.pop();
                        }
                    }
                    if (brackets.isEmpty())
                        return expression;
                }
            }
        }
    }
}
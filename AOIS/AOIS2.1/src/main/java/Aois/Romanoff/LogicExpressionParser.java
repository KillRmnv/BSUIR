package Aois.Romanoff;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LogicExpressionParser {
    private ArrayList<Pattern> expressionPatterns = new ArrayList<>();
    private Matcher expressionMatcher = null;

    LogicExpressionParser() {
        expressionPatterns.add(Pattern.compile("!+\\d"));
        expressionPatterns.add(Pattern.compile("!+\\w"));
        expressionPatterns.add(Pattern.compile("\\(\\d+\\)"));
        expressionPatterns.add(Pattern.compile("\\([\\w+|\\d+]&[\\w+|\\d+]\\)"));
        expressionPatterns.add(Pattern.compile("\\([\\w+|\\d+]\\|[\\w+|\\d+]\\)"));
        expressionPatterns.add(Pattern.compile("\\([\\w+|\\d+]->[\\w+|\\d+]\\)"));
        expressionPatterns.add(Pattern.compile("\\([\\w+|\\d+]~[\\w+|\\d+]\\)"));
        expressionPatterns.add(Pattern.compile("\\w+&\\w+"));
        expressionPatterns.add(Pattern.compile("\\w+\\|\\w+"));
        expressionPatterns.add(Pattern.compile("\\w+->\\w+"));
        expressionPatterns.add(Pattern.compile("\\w+~\\w+"));
    }

    public HashMap<Integer, String> parseOnBasicExpressions(String expression) {
        HashMap<Integer, String> result = new HashMap<>();
        for (int i = 0; i < expressionPatterns.size(); i++) {
            expressionMatcher = expressionPatterns.get(i).matcher(expression);
            if (expressionMatcher.find()) {
                String key = expressionMatcher.group();
                if (i == 8) {
                    result.put(result.size(), key);
                    expression = replaceKeyInExpression(expression, key, result.size());
                } else if (i > 2 && i < 7) {
                    String logicExpression = expressionMatcher.group();
                    int size = key.length();
                    key += "\\(" + key.substring(1, key.length() - 1) + "\\)";
                    key = key.substring(size);
                    logicExpression = logicExpression.substring(1, logicExpression.length() - 1);
                    result.put(result.size(), logicExpression);
                    if (i == 4)
                        expression = replaceKeyInExpression(expression, key, result.size());
                    else
                        expression = expression.replaceAll(key, String.valueOf(result.size() - 1));
                } else {
                    result.put(result.size(), key);
                    expression = expression.replaceAll(key, String.valueOf(result.size() - 1));
                }
                i = 0;
            }
        }
        return result;
    }

    private static String replaceKeyInExpression(String expression, String key, int resultSize) {
        String substringOfExpression = new String(key);
        int j = 1;
        for (; j < key.length() && key.charAt(j) != '|'; j++) ;
        key = key.substring(0, j);
        key += "\\|"; // Экранируем '|'
        key += substringOfExpression.substring(j + 1);
        return expression.replaceAll(key, String.valueOf(resultSize - 1));
    }
}
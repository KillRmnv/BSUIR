package by.romanov.ppois;

import java.lang.reflect.InvocationTargetException;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public interface Input {
    int getChoice(String prompt, int min, int max);
    int getChoice(List<String> prompts, int min, int max);
    String getString(String prompt);
    void show(String message);
    List<Integer> getNumberRange(String prompt,int min, int max);
    String getRegex(String prompt, String regex);
    void showNumericRange(String prompt, int min, int max);
    <K,V>  int getChoiceFromMap(String prompt, Map<K, V> map) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException;
    boolean handleQTE();
    void show(List<String> messages);
    void showNum(int num);
    String getLine(String prompt);
}
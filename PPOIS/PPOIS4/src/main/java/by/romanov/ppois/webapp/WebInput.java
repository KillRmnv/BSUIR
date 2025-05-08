package by.romanov.ppois.webapp;

import by.romanov.ppois.Input;
import lombok.Getter;
import lombok.Setter;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;
import java.util.regex.Pattern;

public class WebInput implements Input {

    @Setter @Getter
    private Map<String, String> params = new HashMap<>();

    @Override
    public int getChoice(String prompt, int min, int max) {
        String value = params.get("choice");
        if (value == null) throw new IllegalArgumentException("Выбор не задан");
        int choice = Integer.parseInt(value);
        if (choice < min || choice > max) {
            throw new IllegalArgumentException("Значение должно быть от " + min + " до " + max);
        }
        return choice;
    }

    @Override
    public int getChoice(List<String> options, int min, int max) {
        String value = params.get("choice");
        if (value == null) throw new IllegalArgumentException("Выбор не задан");
        int choice = Integer.parseInt(value);
        if (choice < min || choice > max) {
            throw new IllegalArgumentException("Значение должно быть от " + min + " до " + max);
        }
        return choice;
    }

    @Override
    public String getString(String key) {
        String value = params.get(key);
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Строка \"" + key + "\" не задана");
        }
        return value;
    }

    @Override
    public List<Integer> getNumberRange(String key, int min, int max) {
        String value = params.get(key);
        if (value == null) throw new IllegalArgumentException("Диапазон не задан");

        String[] parts = value.split("-");
        if (parts.length != 2) throw new IllegalArgumentException("Ожидается формат 'x-y'");

        int a = Integer.parseInt(parts[0].trim());
        int b = Integer.parseInt(parts[1].trim());

        if (a < min || b < min || a > max || b > max || a > b) {
            throw new IllegalArgumentException("Диапазон выходит за пределы допустимого");
        }

        return List.of(a, b);
    }

    @Override
    public String getRegex(String key, String regex) {
        String value = params.get(key);
        if (value == null) throw new IllegalArgumentException("Значение \"" + key + "\" не задано");

        if (!Pattern.matches(regex, value)) {
            throw new IllegalArgumentException("Значение не соответствует шаблону");
        }

        return value;
    }


    @Override
    public <K, V> int getChoiceFromMap(String key, Map<K, V> map)
            throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        String value = params.get("choice");
        if (value == null) throw new IllegalArgumentException("Выбор не задан");
        int index = Integer.parseInt(value);

        if (index < 0 || index >= map.size()) {
            throw new IllegalArgumentException("Недопустимый индекс выбора");
        }

        V selected = (V) map.values().toArray()[index];
        Method info = selected.getClass().getDeclaredMethod("Info");
        if (!info.getReturnType().equals(List.class)) {
            throw new IllegalArgumentException("Метод Info должен возвращать List<String>");
        }
        info.setAccessible(true);
        info.invoke(selected);
        return index;
    }

    @Override
    public boolean handleQTE() {
        return Boolean.parseBoolean(params.getOrDefault("qte", "false"));
    }

    @Override
    public String getLine(String key) {
        return getString(key);
    }
}
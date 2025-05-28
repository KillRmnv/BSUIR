package by.romanov.ppois.Ui;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.val;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ConsoleUserInterface {
    @JsonIgnore
    ConsoleInput input;
    public ConsoleUserInterface() {
        input=new ConsoleInput();
    }
    public ConsoleUserInterface(ConsoleInput input) {
        this.input=input;
    }
    public ConsoleInput getConsoleInput() {
        return input;
    }
    public void setConsoleInput(ConsoleInput input) {
        this.input = input;
    }
    public void show(String message) {
        System.out.println(message);
    }
    public <K, V> void showMap(Map<K, V> map,String prompt) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        System.out.println(prompt);
        List<K> keys = new ArrayList<>();
        int index = 0;
        for (var key : map.keySet()) {
            System.out.println(index + ":");
            Method infoMethod;
            Object value=map.get(key);
            if (isPrimitiveOrWrapper(value.getClass()) || value.getClass().equals(String.class)) {
                System.out.println(value.toString());
            }else {
                try {
                    infoMethod = map.get(key).getClass().getDeclaredMethod("Info");
                } catch (NoSuchMethodException e) {
                    throw new NoSuchMethodException("В множестве значений экземпляров map должен быть реализован метод Info," + " который возвращает List<String> с информацией о полях класса");
                }
                if (!infoMethod.getReturnType().equals(List.class)) {
                    throw new IllegalArgumentException("Метод Info должен возвращать List<String>");
                }
                infoMethod.setAccessible(true);
                List<String> info = (List<String>) infoMethod.invoke(map.get(key));
                for (int i = 0; i < info.size(); i++) {
                    System.out.println(info.get(i));
                }
            }
            keys.add(key);
            index++;
        }
    }
    private boolean isPrimitiveOrWrapper(Class<?> clazz) {
        return clazz.isPrimitive() ||
                clazz.equals(Integer.class) ||
                clazz.equals(Double.class) ||
                clazz.equals(Float.class) ||
                clazz.equals(Long.class) ||
                clazz.equals(Short.class) ||
                clazz.equals(Byte.class) ||
                clazz.equals(Character.class) ||
                clazz.equals(Boolean.class);
    }
    public void showNumericRange(String prompt, int min, int max) {
        System.out.println(prompt);
        System.out.print(min + "-" + max);
        System.out.println();
    }
}
package by.romanov.ppois;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Pattern;

public class ConsoleInput implements Input {
    private Scanner scanner = new Scanner(System.in);

    @Override
    public int getChoice(String prompt, int min, int max) {
        int choice = -1;
        while (true) {
            try {
                System.out.println(prompt);
                choice = scanner.nextInt();
                if (choice < min || choice > max) {
                    throw new Exception("Введите число от " + min + " до " + max);
                }
                break;
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }
        }
        return choice;
    }

    @Override
    public int getChoice(List<String> prompts, int min, int max) {
        int choice = -1;
        for (int index = 0; index < prompts.size(); index++) {
            System.out.println(index + "." + prompts.get(index));
        }
        while (true) {
            try {
                choice = scanner.nextInt();
                if (choice < min || choice > max) {
                    throw new Exception("Введите число от " + min + " до " + max);
                }
                break;
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }
        }
        return choice;
    }

    @Override
    public String getString(String prompt) {
        System.out.println(prompt);
        return scanner.next();
    }

    @Override
    public void show(String message) {
        System.out.println(message);
    }

    @Override
    public List<Integer> getNumberRange(String prompt, int min, int max) {
        System.out.println(prompt);
        List<Integer> numbers = new ArrayList<>();
        while (true) {
            try {

                String choice = scanner.nextLine();
                String[] parts = choice.split("-");

                if (parts.length != 2) {
                    throw new IllegalArgumentException("Некорректный формат строки. Ожидается 'число-число'.");
                }

                int num1 = Integer.parseInt(parts[0].trim());
                int num2 = Integer.parseInt(parts[1].trim());
                if (num1 > max || num2 > max || num1 < min || num2 < min||num1>num2) {
                    throw new RuntimeException("Выход за границы.");
                }
                numbers.add(num1);
                numbers.add(num2);
                break;
            } catch (NumberFormatException e) {
                System.err.println("Ошибка: Оба значения должны быть целыми числами.");
            } catch (IllegalArgumentException e) {
                System.err.println("Ошибка: " + e.getMessage());
            } catch (RuntimeException e) {
                System.err.println("Ошибка: " + e.getMessage());
            }
        }
        return numbers;
    }

    @Override
    public String getRegex(String prompt, String regex) {
        System.out.println(prompt);
        clearBuffer();
        while (true) {
            try {
               String input= scanner.nextLine();
                if (Pattern.compile(regex).matcher(input).find()) {
                    return input;
                } else {
                    throw new RuntimeException(prompt);
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }
        }
    }

    @Override
    public void showNumericRange(String prompt, int min, int max) {
        System.out.println(prompt);
        System.out.print(min + "-" + max);
        System.out.println();
    }

    @Override
    public <K,V> int getChoiceFromMap(String prompt, Map<K, V> map) throws NoSuchMethodException, IllegalArgumentException, InvocationTargetException, IllegalAccessException {
        System.out.println(prompt);
        List<K> keys = new ArrayList<>();
        int index=0;
        for (var key : map.keySet()) {
            System.out.println(index + ":");
            Method infoMethod;
            try {
                infoMethod = map.get(key).getClass().getDeclaredMethod("Info");
            } catch (NoSuchMethodException e) {
                throw new NoSuchMethodException("В множестве значений экземпляров map должен быть реализован метод Info," +
                        " который возвращает List<String> с информацией о полях класса");
            }
            if (!infoMethod.getReturnType().equals(List.class)) {
                throw new IllegalArgumentException("Метод Info должен возвращать List<String>");
            }
            infoMethod.setAccessible(true);
            List<String> info = (List<String>) infoMethod.invoke(map.get(key));
            show(info);
            keys.add(key);
            index++;
        }
        int choiceInt = 0;
        while (true) {
            try {
                choiceInt = scanner.nextInt();
                if (choiceInt>=keys.size()) {
                    throw new Exception("Такого ключа нет");
                }
                break;
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }
        }
        return choiceInt;
    }

    @Override
    public boolean handleQTE() {
        long endTime = System.currentTimeMillis() + 2000;
        try {
            while (System.in.available() > 0) {
                System.in.read();
            }

            while (System.currentTimeMillis() < endTime) {
                if (System.in.available() > 0) {
                    int input = System.in.read();
                    if (input == ' ' || input == '\n' || input == '\r') {
                        return true;
                    }
                }
                Thread.sleep(10);
            }
        } catch (IOException e) {
            System.err.println("Ошибка ввода: " + e.getMessage());
            return false;
        } catch (InterruptedException e) {
            System.err.println("Прерывание потока: " + e.getMessage());
            return false;
        }
        return false;
    }

    @Override
    public void show(List<String> messages) {
        for (int index = 0; index < messages.size(); index++) {
            System.out.println(messages.get(index));
        }
    }
    @Override
    public void showNum(int num){
        System.out.print(num+".");
    }

    @Override
    public String getLine(String prompt) {
        System.out.println(prompt);
        clearBuffer();
        return scanner.nextLine();
    }
    public void clearBuffer() {
        if (!scanner.hasNext()) {
            return;
        }

        if (scanner.hasNext("\\R")) {
            scanner.nextLine();
        }
        scanner.skip("\\s*");
    }
}
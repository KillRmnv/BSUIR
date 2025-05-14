package by.romanov.ppois.Ui;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Pattern;

public class ConsoleInput {
    private Scanner scanner = new Scanner(System.in);

    public int getChoice(String prompt, int min, int max) {
        int choice = -1;
        while (true) {
            try {
                System.out.println("(от "+min+" до " + max+")\n"+prompt);
                String input = scanner.nextLine();
                choice = Integer.parseInt(input);
                if (choice < min || choice > max) {
                    System.out.println("Введите число от " + min + " до " + max);
                } else {
                    break;
                }
            } catch (NumberFormatException e) {
                System.out.println("Ошибка: Введите целое число.");
            }
        }
        return choice;
    }

    public int getChoice(List<String> prompts, int min, int max) {
        int choice = -1;
        for (int index = 0; index < prompts.size(); index++) {
            System.out.println(index + "." + prompts.get(index));
        }
        while (true) {
            try {
                String input = scanner.nextLine();
                choice = Integer.parseInt(input);
                if (choice < min || choice > max) {
                    System.out.println("Введите число от " + min + " до " + max);
                } else {
                    break;
                }
            } catch (NumberFormatException e) {
                System.out.println("Ошибка: Введите целое число.");
            }
        }
        return choice;
    }

    public String getString(String prompt) {
        System.out.println(prompt);
        return scanner.next();
    }

    public List<Integer> getNumberRange(String prompt, int min, int max) {
        System.out.println(prompt);
        List<Integer> numbers = new ArrayList<>();
        while (true) {
            try {
                String choice = scanner.nextLine();
                String[] parts = choice.split("-");
                if (parts.length != 2) {
                    System.out.println("Некорректный формат строки. Ожидается 'число-число'.");
                    continue;
                }
                int num1 = Integer.parseInt(parts[0].trim());
                int num2 = Integer.parseInt(parts[1].trim());
                if (num1 > max || num2 > max || num1 < min || num2 < min || num1 > num2) {
                    System.out.println("Выход за границы.");
                    continue;
                }
                numbers.add(num1);
                numbers.add(num2);
                break;
            } catch (NumberFormatException e) {
                System.out.println("Ошибка: Оба значения должны быть целыми числами.");
            }
        }
        return numbers;
    }

    public String getRegex(String prompt, String regex) {
        System.out.println(prompt);
        clearBuffer();
        while (true) {
            try {
                String input = scanner.nextLine();
                if (Pattern.compile(regex).matcher(input).find()) {
                    return input;
                } else {
                    System.out.println(prompt);
                }
            } catch (Exception e) {
                System.out.println("Ошибка: " + e.getMessage());
            }
        }
    }

    public <K, V> int getChoiceFromMap(String prompt, Map<K, V> map) {
        System.out.println(prompt);
        int choiceInt = 0;
        while (true) {
            try {
                String input = scanner.nextLine();
                choiceInt = Integer.parseInt(input);
                if (choiceInt >= map.keySet().size()) {
                    System.out.println("Такого ключа нет");
                    continue;
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Ошибка: Введите целое число.");
            }
        }
        return choiceInt;
    }

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
                        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
                        while (reader.ready()) {
                            reader.read();
                        }
                        return true;
                    }
                }
                Thread.sleep(10);
            }
        } catch (IOException e) {
            System.out.println("Ошибка ввода: " + e.getMessage());
            return false;
        } catch (InterruptedException e) {
            System.out.println("Прерывание потока: " + e.getMessage());
            return false;
        }

        return false;
    }

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
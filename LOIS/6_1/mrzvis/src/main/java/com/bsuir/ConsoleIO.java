/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Алгоритм вычисления целочисленного частного пары 4-разрядных чисел делением без восстановления частичного остатка
Файл реализующий класс реализующий детализированный табличный выводом
Источники:
(1) Интеграционная платформа
*/

package com.bsuir;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class ConsoleIO {

    private Scanner scanner = new Scanner(System.in);
    private Random random = new Random();

    public void inputPipelineParams() {
        System.out.println("НАСТРОЙКА ПАЙПЛАЙНА");

        Config.amountOfPairs = readSafeInt(
            "m - длина вектора (кол-во пар): ",
            1
        );
        Config.parallelism = readSafeInt("r - ранг задачи (параллелизм): ", 1);
        Config.amountOfBits = readSafeInt("p - разряды (количество бит): ", 1);
        Config.tactTime = readSafeInt("ti - тактов на этап: ", 1);
    }

    private int readSafeInt(String message, int minValue) {
        int value;
        while (true) {
            System.out.print(message);

            if (scanner.hasNextInt()) {
                value = scanner.nextInt();

                if (value >= minValue) {
                    return value;
                } else {
                    System.out.println(
                        "Ошибка: значение должно быть >= " + minValue
                    );
                }
            } else {
                System.out.println("Ошибка: введите целое число.");
                scanner.next();
            }
        }
    }

    public Pair generateRandomPair() {
        int maxVal = (1 << (Config.amountOfBits - 1)) - 1;
        int dividend = random.nextInt(maxVal) + 1;
        int divisor = random.nextInt(maxVal) + 1;

        BinaryNumber first = new BinaryNumber(
            dividend,
            Config.amountOfBits * 2
        );
        BinaryNumber second = new BinaryNumber(
            divisor,
            Config.amountOfBits * 2
        );

        System.out.println(
            dividend +
                " : " +
                divisor +
                " ~ " +
                toBinaryString(first) +
                " : " +
                toBinaryString(second)
        );

        return new Pair(first, second);
    }

    public void displayState(
        int tact,
        List<Stage> stages,
        List<Pair> completedPairs
    ) {
        if (!completedPairs.isEmpty() && tact > 0) {
            System.out.println("\nВЫПОЛНЕННЫЕ ПАРЫ:");
            for (Pair pair : completedPairs) {
                if (pair.getCompletionTact() == tact) {
                    displayCompletedPair(pair);
                }
            }
        }

        System.out.println(" ТАКТ: " + tact);
        System.out.println(
            "ЭТАП    | №   | A (" +
                Config.amountOfBits +
                "б) | Q (" +
                Config.amountOfBits +
                "б) | M (" +
                Config.amountOfBits +
                "б) | СТАТУС"
        );
        System.out.println(
            "-----------------------------------------------------------------"
        );

        for (int i = 0; i < stages.size(); i++) {
            Stage stage = stages.get(i);
            System.out.print(String.format("Этап %-3d | ", i));
            if (!stage.isComplete()) {
                List<Pair> pairs = stage.getPairs();
                if (!pairs.isEmpty()) {
                    displayPairState(pairs.get(0));
                    int prefixWidth = "Этап %-3d".length();
                    for (int pair = 1; pair < pairs.size(); pair++) {
                        System.out.print(" ".repeat(prefixWidth) + "| ");
                        displayPairState(pairs.get(pair));
                    }
                }
            } else {
                System.out.println("-   | -    | -    | -    | [ Свободен ]");
            }
        }
        System.out.println(
            "-----------------------------------------------------------------"
        );
    }

    private void displayPairState(Pair pair) {
        int p = Config.amountOfBits;
        int[] bits2=pair.getStateBeforeOp().getBits();
        int[] aBits = Arrays.copyOfRange(bits2,p, 2*p);
        int[] qBits = Arrays.copyOfRange(bits2, 0, p);
        int[] reversedArray = new int[qBits.length];
        for (int i = 0; i < qBits.length; i++) {
            reversedArray[i] = qBits[qBits.length - 1 - i];
        }
        BinaryNumber aNum = new BinaryNumber(aBits);
        BinaryNumber qNum = new BinaryNumber(qBits);

        BinaryNumber divisor = pair.getDivisor();
        int[] mBits = Arrays.copyOfRange(divisor.getBits(), 0, p);
        BinaryNumber mNum = new BinaryNumber(mBits);

        String aStr = toBinaryString(aNum);
        String qStr = toBinaryString(qNum);
        String mStr = toBinaryString(mNum);

        String status = "";
        if (!pair.getOperation().isEmpty()) {
            status = pair.getOperation() + ", bit=" + pair.getCurrentBit();
        }

        System.out.println(
            String.format(
                "%-3d | %-4s | %-4s | %-4s | %s",
                pair.getPairNumber(),
                aStr,
                qStr,
                mStr,
                status
            )
        );
    }

    private void displayCompletedPair(Pair pair) {
        int p = Config.amountOfBits;
        BinaryNumber result = pair.getFirst();
        int[] bits = result.getBits();

        int[] qBits = Arrays.copyOfRange(bits, 0, p);
        int[] rBits = Arrays.copyOfRange(bits, p, 2 * p);

        BinaryNumber qNum = new BinaryNumber(qBits);
        BinaryNumber rNum = new BinaryNumber(rBits);

        int q = binaryToInt(qNum);
        int r = binaryToInt(rNum);

        int[] mBits = Arrays.copyOfRange(pair.getDivisor().getBits(), 0, p);
        BinaryNumber mNum = new BinaryNumber(mBits);
        int m = binaryToInt(mNum);

        System.out.println(
            String.format(
                "   Пара %d завершена: Q=%d, R=%d, M=%d (такт %d)",
                pair.getPairNumber(),
                q,
                r,
                m,
                pair.getCompletionTact()
            )
        );
    }

    public void displayFinalResults(List<Pair> pairs) {
        System.out.println(
            "\n                         ИТОГОВЫЕ РЕЗУЛЬТАТЫ                         "
        );
        System.out.println(
            "№   | Q (bin) | Q (dec) | R (bin) | R (dec) | M (bin) | M (dec) | Такт"
        );
        System.out.println(
            "------------------------------------------------------------------------"
        );

        for (Pair pair : pairs) {
            int p = Config.amountOfBits;
            BinaryNumber result = pair.getFirst();
            int[] bits = result.getBits();

            int[] qBits = Arrays.copyOfRange(bits, 0, p);
            int[] rBits = Arrays.copyOfRange(bits, p, 2 * p);

            BinaryNumber qNum = new BinaryNumber(qBits);
            BinaryNumber rNum = new BinaryNumber(rBits);

            int q = binaryToInt(qNum);
            int r = binaryToInt(rNum);

            int[] mBits = Arrays.copyOfRange(pair.getDivisor().getBits(), 0, p);
            BinaryNumber mNum = new BinaryNumber(mBits);
            int m = binaryToInt(mNum);

            System.out.println(
                String.format(
                    "%-3d | %-7s | %-7d | %-7s | %-7d | %-7s | %-7d |",
                    pair.getPairNumber(),
                    toBinaryString(qNum),
                    q,
                    toBinaryString(rNum),
                    r,
                    toBinaryString(mNum),
                    m
                )
            );
        }
    }

    private String toBinaryString(BinaryNumber num) {
        StringBuilder sb = new StringBuilder();
        int[] bits = num.getBits();
        for (int i = bits.length - 1; i >= 0; i--) {
            sb.append(bits[i]);
        }
        return sb.toString();
    }

    private int binaryToInt(BinaryNumber num) {
        int[] bits = num.getBits();
        int result = 0;

        for (int i = 0; i < bits.length; i++) {
            result += bits[i] * (1 << i);
        }

        return result;
    }
}

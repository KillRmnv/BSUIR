package com.bsuir;

import java.util.Scanner;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class ConsoleIO {
    
    private Scanner scanner = new Scanner(System.in);
    private Random random = new Random();
    
    public void inputPipelineParams() {
        System.out.println("НАСТРОЙКА ПАЙПЛАЙНА");
    
        Config.amountOfPairs = readSafeInt("m - длина вектора (кол-во пар): ", 1);
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
                    System.out.println("Ошибка: значение должно быть >= " + minValue);
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
        
        BinaryNumber first = new BinaryNumber(dividend, Config.amountOfBits*2);
        
        BinaryNumber second = new BinaryNumber(divisor, Config.amountOfBits*2);
        System.out.println( dividend + " : "+divisor+ " ~ "+toString(first) + " : " + toString(second));
        
        return new Pair(first, second);
    }
    
    public void displayState(int tact, List<Stage> stages) {
        System.out.println("\n Такт " + tact );
        
        for (int i = 0; i < stages.size(); i++) {
            Stage stage = stages.get(i);
            System.out.print("Этап " + i + ": ");
            
            if (!stage.isComplete()) {
                List<Pair> pairs = stage.getPairs();
                for (Pair pair : pairs) {
                    System.out.print("[A=" + toString(pair.getFirst()) 
                        + " B=" + toString(pair.getSecond()) + "] ");
                }
            } else {
                System.out.print("пусто");
            }
            System.out.println();
        }
    }
    
    public void displayResult(int pairNum, Pair pair) {
        BinaryNumber res = pair.getFirst();
        BinaryNumber divisorBin = pair.getSecond();
        
        System.out.println("\n РЕЗУЛЬТАТ пары " + pairNum );
        
        int p = Config.amountOfBits;
        int[] bits = res.getBits();
        
        int[] quotientBits = Arrays.copyOfRange(bits, 0, p);
        int[] remainderBits = Arrays.copyOfRange(bits, p, 2 * p);
        
        BinaryNumber quotientNum = new BinaryNumber(quotientBits);
        BinaryNumber remainderNum = new BinaryNumber(remainderBits);
        
        int quotient = binaryToInt(quotientNum);
        int remainder = binaryToInt(remainderNum);
            
        System.out.println("Частное: " + toString(quotientNum));
        System.out.println("Частное (dec): " + quotient);
        System.out.println("Остаток: " + toString(remainderNum));
        System.out.println("Остаток (dec): " + remainder);
    }
    public void displayResults( List<Pair> pairs) {
        for (int i = 0; i < pairs.size(); i++) {
            
            displayResult(i + 1, pairs.get(i));
        }
    }
    private String toString(BinaryNumber num) {
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
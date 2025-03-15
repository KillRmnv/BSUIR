package Aois.Romanoff;

import java.util.Scanner;

public class ConsoleIOHandler implements IOHandler {
    private final Scanner scanner;

    public ConsoleIOHandler(Scanner scanner) {
        this.scanner = scanner;
    }

    @Override
    public int readInt(String prompt) {
        System.out.print(prompt);
        return scanner.nextInt();
    }

    @Override
    public double readDouble(String prompt) {
        System.out.print(prompt);
        return scanner.nextDouble();
    }

    @Override
    public void print(String message) {
        System.out.println(message);
    }
}

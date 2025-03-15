package Aois.Romanoff;
import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        IOHandler ioHandler = new ConsoleIOHandler(scanner);
        BinConverter binConverter = new BinConverter();
        DecimalConverter decimalConverter = new DecimalConverter();

        UI ui = new UI(ioHandler, binConverter, decimalConverter);
        ui.run();
    }
}

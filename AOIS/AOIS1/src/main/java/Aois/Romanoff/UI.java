package Aois.Romanoff;
import java.util.ArrayList;

public class UI {
    private final IOHandler ioHandler;
    private final BinConverter binConverter;
    private final DecimalConverter decimalConverter;

    public UI(IOHandler ioHandler, BinConverter binConverter, DecimalConverter decimalConverter) {
        this.ioHandler = ioHandler;
        this.binConverter = binConverter;
        this.decimalConverter = decimalConverter;
    }

    public void run() {
        while (true) {
            ioHandler.print("1. Бинарное число в прямом, обратном и дополнительном коде");
            ioHandler.print("2. Сложение двух чисел");
            ioHandler.print("3. Вычитание двух чисел");
            ioHandler.print("4. Умножение двух чисел");
            ioHandler.print("5. Деление двух чисел");
            ioHandler.print("6. Сложение двух положительных чисел с плавающей точкой");
            ioHandler.print("7. Завершить работу");

            int choice = ioHandler.readInt("Выберите действие (1-7): ");
            switch (choice) {
                case 1 -> {
                    handleBinaryConversion();
                }
                case 2 -> {
                    handleAddition();
                }
                case 3 -> {
                    handleSubtraction();
                }
                case 4 -> {
                    handleMultiplication();
                }
                case 5 -> {
                    handleDivision();
                }
                case 6 -> {
                    handleFloatAddition();
                }
                case 7 -> {
                    ioHandler.print("Завершение работы.");
                    return;
                }
                default -> ioHandler.print("Некорректный выбор. Пожалуйста, выберите номер от 1 до 7.");
            }
        }
    }

    public void handleBinaryConversion() {
        int num = ioHandler.readInt("Введите число: ");
        BinNumber number = new BinNumber();
        number.Setter(binConverter.ConvertToBin(num));
        ioHandler.print("Прямой код: " + number.Getter());
        ioHandler.print("Обратный код: " + number.convertToOneComplmnt());
        ioHandler.print("Дополнительный код: " + number.convertToTwoComplmnt());
    }

    public void handleAddition() {
        int num1 = ioHandler.readInt("Введите первое число: ");
        int num2 = ioHandler.readInt("Введите второе число: ");
        BinNumber number1 = new BinNumber();
        number1.Setter(binConverter.ConvertToBin(num1));
        BinNumber number2 = new BinNumber();
        number2.Setter(binConverter.ConvertToBin(num2));
        ArrayList<Integer> sum = number1.Adding(number2.Getter());
        ioHandler.print("Результат сложения: " + sum);
        number1.Setter(sum);
        ioHandler.print("Результат сложения в десятичной СИ: " + decimalConverter.ConvertFrBinToDecimal(number1.Getter()));
    }

    public void handleSubtraction() {
        int num1 = ioHandler.readInt("Введите первое число: ");
        int num2 = ioHandler.readInt("Введите второе число: ");
        BinNumber number1 = new BinNumber();
        number1.Setter(binConverter.ConvertToBin(num1));
        BinNumber number2 = new BinNumber();
        number2.Setter(binConverter.ConvertToBin(num2));
        ArrayList<Integer> result = number1.Subtracting(number2.Getter());
        ioHandler.print("Результат вычитания: " + result);
        number1.Setter(result);
        ioHandler.print("Результат вычитания в десятичной СИ: " + decimalConverter.ConvertFrBinToDecimal(number1.Getter()));
    }

    public void handleMultiplication() {
        int num1 = ioHandler.readInt("Введите первое число: ");
        int num2 = ioHandler.readInt("Введите второе число: ");
        BinNumber number1 = new BinNumber();
        number1.Setter(binConverter.ConvertToBin(num1));
        BinNumber number2 = new BinNumber();
        number2.Setter(binConverter.ConvertToBin(num2));
        ArrayList<Integer> result = number1.multiplication(number2.Getter());
        ioHandler.print("Результат умножения: " + result);
        number1.Setter(result);
        ioHandler.print("Результат умножения в десятичной СИ: " + decimalConverter.ConvertFrBinToDecimal(number1.Getter()));
    }

    public void handleDivision() {
        int num1 = ioHandler.readInt("Введите первое число: ");
        int num2 = ioHandler.readInt("Введите второе число: ");
        BinNumber number1 = new BinNumber();
        number1.Setter(binConverter.ConvertToBin(num1));
        BinNumber number2 = new BinNumber();
        number2.Setter(binConverter.ConvertToBin(num2));
        ArrayList<Integer> result = number1.division(number2.Getter());
        BinFixPointNum fixPointNum = new BinFixPointNum();
        fixPointNum.Setter(result);
        ioHandler.print("Результат деления: " + result);
        ioHandler.print("Результат деления в десятичной СИ: " + decimalConverter.ConvertFrFixPntToDecimal(fixPointNum.Getter()));
    }

    public void handleFloatAddition() {
        double num1 = ioHandler.readDouble("Введите первое положительное число: ");
        double num2 = ioHandler.readDouble("Введите второе положительное число: ");
        BinFloatPointNum numberFloat1 = new BinFloatPointNum();
        numberFloat1.Setter(binConverter.ConvertToFloatBin(num1));
        BinFloatPointNum numberFloat2 = new BinFloatPointNum();
        numberFloat2.Setter(binConverter.ConvertToFloatBin(num2));
        ArrayList<Integer> result = numberFloat1.Adding(numberFloat2.Getter());
        BinFloatPointNum floatPointNum = new BinFloatPointNum();
        floatPointNum.Setter(result);
        ioHandler.print("Результат сложения: " + result);
        ioHandler.print("Результат сложения в десятичной СИ: " + decimalConverter.ConvertFrFloatPntToDecimal(floatPointNum.Getter()));
    }
}
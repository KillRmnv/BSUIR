package Aois.Romanoff;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.Mockito.*;
public class UITest {
    @Test
    void testHandleBinaryConversion() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readInt("Введите число: ")).thenReturn(10);
        when(binConverter.ConvertToBin(10)).thenReturn(new ArrayList<>(List.of(0,1, 0, 1, 0)));

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleBinaryConversion();

        verify(ioHandler).print("Прямой код: [0, 1, 0, 1, 0]");
        verify(ioHandler).print("Обратный код: [0, 1, 0, 1, 0]");
        verify(ioHandler).print("Дополнительный код: [0, 1, 0, 1, 0]");
    }
    @Test
    void testHandleAddition() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readInt("Введите первое число: ")).thenReturn(5);
        when(ioHandler.readInt("Введите второе число: ")).thenReturn(3);
        when(binConverter.ConvertToBin(5)).thenReturn(new ArrayList<>(List.of(0,1, 0, 1)));
        when(binConverter.ConvertToBin(3)).thenReturn(new ArrayList<>(List.of(0, 1, 1)));

        BinNumber binNumber = mock(BinNumber.class);
        when(binNumber.Adding(any())).thenReturn(new ArrayList<>(List.of(0,1, 0, 0, 0)));

        when(decimalConverter.ConvertFrBinToDecimal(any())).thenReturn((double)8);

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleAddition();

        verify(ioHandler).print("Результат сложения: [0, 1, 0, 0, 0]");
        verify(ioHandler).print("Результат сложения в десятичной СИ: 8.0");
    }
    @Test
    void testHandleSubtraction() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readInt("Введите первое число: ")).thenReturn(10);
        when(ioHandler.readInt("Введите второе число: ")).thenReturn(5);
        when(binConverter.ConvertToBin(10)).thenReturn(new ArrayList<>(List.of(0,1, 0, 1, 0)));
        when(binConverter.ConvertToBin(5)).thenReturn(new ArrayList<>(List.of(0, 1, 0, 1)));

        BinNumber binNumber = mock(BinNumber.class);
        when(binNumber.Subtracting(any())).thenReturn(new ArrayList<>(List.of(0, 1, 0, 1)));

        when(decimalConverter.ConvertFrBinToDecimal(any())).thenReturn((double)5);

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleSubtraction();

        verify(ioHandler).print("Результат вычитания: [0, 0, 1, 0, 1]");
        verify(ioHandler).print("Результат вычитания в десятичной СИ: 5.0");
    }
    @Test
    void testHandleMultiplication() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readInt("Введите первое число: ")).thenReturn(4);
        when(ioHandler.readInt("Введите второе число: ")).thenReturn(3);
        when(binConverter.ConvertToBin(4)).thenReturn(new ArrayList<>(List.of(0, 1, 0, 0)));
        when(binConverter.ConvertToBin(3)).thenReturn(new ArrayList<>(List.of(0, 1, 1)));

        BinNumber binNumber = mock(BinNumber.class);
        when(binNumber.multiplication(any())).thenReturn(new ArrayList<>(List.of(0, 1, 1, 0, 0)));

        when(decimalConverter.ConvertFrBinToDecimal(any())).thenReturn((double)12);

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleMultiplication();

        verify(ioHandler).print("Результат умножения: [0, 1, 1, 0, 0]");
        verify(ioHandler).print("Результат умножения в десятичной СИ: 12.0");
    }
    @Test
    void testHandleDivision() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readInt("Введите первое число: ")).thenReturn(10);
        when(ioHandler.readInt("Введите второе число: ")).thenReturn(2);
        when(binConverter.ConvertToBin(10)).thenReturn(new ArrayList<>(List.of(0, 1, 0, 1, 0)));
        when(binConverter.ConvertToBin(2)).thenReturn(new ArrayList<>(List.of(0, 1, 0)));

        BinNumber binNumber = mock(BinNumber.class);
        when(binNumber.division(any())).thenReturn(new ArrayList<>(List.of(0, 1, 0, 1)));

        when(decimalConverter.ConvertFrFixPntToDecimal(any())).thenReturn(5.0);

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleDivision();

        verify(ioHandler).print("Результат деления: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]");
        verify(ioHandler).print("Результат деления в десятичной СИ: 5.0");
    }
    @Test
    void testHandleFloatAddition() {
        IOHandler ioHandler = mock(IOHandler.class);
        BinConverter binConverter = mock(BinConverter.class);
        DecimalConverter decimalConverter = mock(DecimalConverter.class);

        when(ioHandler.readDouble("Введите первое положительное число: ")).thenReturn(2.5);
        when(ioHandler.readDouble("Введите второе положительное число: ")).thenReturn(3.5);
        when(binConverter.ConvertToFloatBin(2.5)).thenReturn(new ArrayList<>(List.of(0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)));
        when(binConverter.ConvertToFloatBin(3.5)).thenReturn(new ArrayList<>(List.of(0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)));

        BinFloatPointNum binFloatPointNum = mock(BinFloatPointNum.class);
        when(binFloatPointNum.Adding(any())).thenReturn(new ArrayList<>(List.of(0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)));

        when(decimalConverter.ConvertFrFloatPntToDecimal(any())).thenReturn(6.0);

        UI ui = new UI(ioHandler, binConverter, decimalConverter);

        ui.handleFloatAddition();

        verify(ioHandler).print("Результат сложения: [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]");
        verify(ioHandler).print("Результат сложения в десятичной СИ: 6.0");
    }
}

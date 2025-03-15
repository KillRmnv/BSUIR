package Aois.Romanoff;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BinFixPointNumTest {

    @Test
    void testConvert() {
        BinFixPointNum binNum = new BinFixPointNum();
        BinConverter binConverter = new BinConverter();
        DecimalConverter decimalConverter = new DecimalConverter();
        binNum.Setter(binConverter.ConvertToFixBin(10.75));
        double result =  decimalConverter.ConvertFrFixPntToDecimal(binNum.Getter());
        assertEquals(10.75, result, 0.00001, "Ошибка при преобразовании в десятичный формат");
    }
}

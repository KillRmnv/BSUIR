package org.example;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class BinFloatPointTest {
    @Test
    public void testConvert() {
        BinConverter binConverter = new BinConverter();
        ArrayList<Integer> expected = new ArrayList<>(Arrays.asList(0,1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1,1,1,1,0,1));
        BinFloatPointNum num = new BinFloatPointNum();
        num.Setter(binConverter.ConvertToFloatBin(14.88));
        assertEquals(expected, num.Getter());
    }
    @Test
    void testAdding() {
        ArrayList<Integer> sum;
        BinConverter binConverter = new BinConverter();
        DecimalConverter decimalConverter = new DecimalConverter();
        BinFloatPointNum numFloat1 = new BinFloatPointNum();
        numFloat1.Setter(binConverter.ConvertToFloatBin(6.43));
        System.out.println(decimalConverter.ConvertFrFloatPntToDecimal(numFloat1.Getter()));
        BinFloatPointNum numFloat2 = new BinFloatPointNum();
        numFloat2.Setter(binConverter.ConvertToFloatBin(3.14));
        System.out.println(decimalConverter.ConvertFrFloatPntToDecimal(numFloat2.Getter()));

        sum = numFloat1.Adding(numFloat2.Getter());
        numFloat1.Setter(sum);
        assertEquals(9.57,decimalConverter.ConvertFrFloatPntToDecimal(numFloat1.Getter()),0.001);
    }
}

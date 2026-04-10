/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Алгоритм вычисления целочисленного частного пары 4-разрядных чисел делением без восстановления частичного остатка
Файл реализующий класс бинарного числа
Источники:
(1) Интеграционная платформа

14.03.2026

 */
package com.bsuir;

public class BinaryNumber {

    private int[] bits;

    public int[] getBits() {
        return bits;
    }

    public void setBits(int[] bits) {
        this.bits = bits;
    }
    public BinaryNumber clone() {
        return new BinaryNumber(bits.clone());
    }

    public BinaryNumber(int[] bits) {
        this.bits = bits;
    }
    public BinaryNumber(int[] bits,int size) {
        this.bits = new int[size];
        for(int i=bits.length/2; i < size; i++) {
            this.bits[i] = bits[i];
        }
    }
    public BinaryNumber(int number,int size) {
        this.bits = new int[size];
        for (int i = 0; i < size; i++) {
            bits[i] = (number >> i) & 1;
        }
    }

    public BinaryNumber(int size) {
        this.bits = new int[size];
    }

    public BinaryNumber add(BinaryNumber other) {
        int[] result = new int[bits.length];  
        int carry = 0;
        for (int i = 0; i < bits.length; i++) {  
            int sum = carry + bits[i] + other.bits[i];
            result[i] = sum % 2;
            carry = sum / 2;
        }
        
        return new BinaryNumber(result);
    }
    
    public BinaryNumber subtract(BinaryNumber other) {
        int[] result = new int[bits.length];
        int borrow = 0;
        for (int i = 0; i < bits.length; i++) {
            int diff = bits[i] - other.bits[i] + borrow;
            if (diff < 0) {
                diff += 2;
                borrow = -1;
            } else {
                borrow = 0;
            }
            result[i] = diff;
        }
        return new BinaryNumber(result);
    }
    public void shiftLeft() {
        for (int i = bits.length - 1; i > 0; i--) {
            bits[i] = bits[i - 1];
        }
        bits[0] = 0;
    }
    public void setBit(int index, int value) {
        bits[index] = value;
    }
    public int size() {
        return bits.length;
    }
    public void fromInt(int value) {
        for (int i = 0; i < bits.length; i++) {
            bits[i] = (value >> i) & 1;
        }
    }

    public String toBinaryString() {
        StringBuilder sb = new StringBuilder();
        for (int i = bits.length - 1; i >= 0; i--) {
            sb.append(bits[i]);
        }
        return sb.toString();
    }

    public String toBinaryString(int from, int to) {
        StringBuilder sb = new StringBuilder();
        for (int i = to - 1; i >= from; i--) {
            sb.append(bits[i]);
        }
        return sb.toString();
    }

    public int toInt() {
        int result = 0;
        for (int i = 0; i < bits.length; i++) {
            result += bits[i] * (1 << i);
        }
        return result;
    }
}
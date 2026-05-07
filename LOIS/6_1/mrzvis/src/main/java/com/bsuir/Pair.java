/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Файл реализующий класс пары информацией для отслеживания состояния
*/

package com.bsuir;

public class Pair {
    private BinaryNumber first;
    private BinaryNumber second;
    private BinaryNumber divisor;
    private int pairNumber;
    private int completionTact;
    private BinaryNumber stateBeforeOp; 
    private String operation; 
    private int currentBit; 
    public Pair(BinaryNumber first, BinaryNumber second) {
        this.first = first;
        this.second = second;
        this.divisor = second.clone(); 
        this.pairNumber = -1;
        this.completionTact = -1;
        this.stateBeforeOp = null;
        this.operation = "";
        this.currentBit = -1;
    }
    
    public BinaryNumber getFirst() {
        return first;
    }
    
    public void setFirst(BinaryNumber first) {
        this.first = first;
    }
    
    public BinaryNumber getSecond() {
        return second;
    }
    
    public void setSecond(BinaryNumber second) {
        this.second = second;
    }
    
    public BinaryNumber getDivisor() {
        return divisor;
    }
    
    public int getPairNumber() {
        return pairNumber;
    }
    
    public void setPairNumber(int pairNumber) {
        this.pairNumber = pairNumber;
    }
    
    public int getCompletionTact() {
        return completionTact;
    }
    
    public void setCompletionTact(int completionTact) {
        this.completionTact = completionTact;
    }
    
    public BinaryNumber getStateBeforeOp() {
        return stateBeforeOp;
    }
    
    public void setStateBeforeOp(BinaryNumber stateBeforeOp) {
        this.stateBeforeOp = stateBeforeOp;
    }
    
    public String getOperation() {
        return operation;
    }
    
    public void setOperation(String operation) {
        this.operation = operation;
    }
    
    public int getCurrentBit() {
        return currentBit;
    }
    
    public void setCurrentBit(int currentBit) {
        this.currentBit = currentBit;
    }
}
package com.bsuir;

public class Pair {

    private BinaryNumber first;
    private BinaryNumber second;

    public Pair(BinaryNumber first, BinaryNumber second) {
        this.first = first;
        this.second = second;
    }
    public void setFirst(BinaryNumber first) {
        this.first = first;
    }

    public void setSecond(BinaryNumber second) {
        this.second = second;
    }
    public BinaryNumber getFirst() {
        return first;
    }

    public BinaryNumber getSecond() {
        return second;
    }
}

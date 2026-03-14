package com.bsuir;

import java.util.List;
import java.util.concurrent.CountDownLatch;

public class Stage {

    private boolean isLast;
    private List<Pair> pairs;

    public Stage() {
        pairs = null;
        isLast = false;
    }

    public Stage(boolean isLast) {
        pairs = null;
        this.isLast = isLast;
    }

    public Stage(List<Pair> pairs, boolean isLast) {
        this.pairs = pairs;
        this.isLast = isLast;
    }

    public boolean isComplete() {
        return pairs == null;
    }

    public boolean isLast() {
        return isLast;
    }

    public List<Pair> getPairs() {
        return pairs;
    }

    public void setPairs(List<Pair> pairs) {
        this.pairs = pairs;
    }

    public void execute() throws InterruptedException {
        if (pairs == null || pairs.isEmpty()) return;

        CountDownLatch latch = new CountDownLatch(pairs.size());

        for (Pair pair : pairs) {
            new Thread(() -> {
                BinaryNumber a = pair.getFirst();
                BinaryNumber b = pair.getSecond().clone();
                int p = Config.amountOfBits;
                int size = a.size(); 

                BinaryNumber bAligned = new BinaryNumber(size);
                for (int i = 0; i < p; i++) {
                    bAligned.setBit(p + i, b.getBits()[i]);
                }

                try {
                    BinaryNumber result;

                    if (a.getBits()[size - 1] == 1) {
                        a.shiftLeft();
                        result = a.add(bAligned);
                    } else {
                        a.shiftLeft();
                        result = a.subtract(bAligned);
                    }

                    if (result.getBits()[size - 1] == 1) {
                        result.setBit(0, 0);
                    } else {
                        result.setBit(0, 1);
                    }

                    if (isLast && result.getBits()[size - 1] == 1) {
                        result = result.add(bAligned);
                    }

                    pair.setFirst(result);
                } finally {
                    latch.countDown();
                }
            })
                .start();
        }

        latch.await();
    }

    private void changeBit(BinaryNumber result, int size) {
        if (result.getBits()[size - 1] == 1) {
            result.setBit(0, 0);
        } else {
            result.setBit(0, 1);
        }
    }

    private BinaryNumber addSubstact(BinaryNumber first, BinaryNumber second) {
        int size = first.size();

        if (first.getBits()[size - 1] == 1) {
            return first.add(second);
        } else {
            return first.subtract(second);
        }
    }

    public void eject() {
        pairs = null;
    }
}

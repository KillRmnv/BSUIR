/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Алгоритм вычисления целочисленного частного пары 4-разрядных чисел делением без восстановления частичного остатка

Данный файл реализует класс этапа конвеера
Источники:
(1) Интеграционная платформа
14.03.2026
*/

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
                BinaryNumber aOriginal = pair.getFirst();
                int p = Config.amountOfBits;

                BinaryNumber a;
                if (aOriginal.size() == p * 2) {
                    a = new BinaryNumber(p * 2 + 1);
                    for (int i = 0; i < p * 2; i++) {
                        a.setBit(i, aOriginal.getBits()[i]);
                    }
                } else {
                    a = aOriginal;
                }

                int size = a.size();
                BinaryNumber b = pair.getSecond().clone();

                pair.setStateBeforeOp(a.clone());

                BinaryNumber bAligned = new BinaryNumber(size);
                for (int i = 0; i < p; i++) {
                    bAligned.setBit(p + i, b.getBits()[i]);
                }

                try {
                    BinaryNumber result;
                    if (a.getBits()[size - 1] == 1) {
                        a.shiftLeft();
                        result = a.add(bAligned);
                        pair.setOperation("+M");
                    } else {
                        a.shiftLeft();
                        result = a.subtract(bAligned);
                        pair.setOperation("-M");
                    }

                    if (result.getBits()[size - 1] == 1) {
                        result.setBit(0, 0);
                        pair.setCurrentBit(0);
                    } else {
                        result.setBit(0, 1);
                        pair.setCurrentBit(1);
                    }

                    if (isLast && result.getBits()[size - 1] == 1) {
                        result = result.add(bAligned);
                        pair.setOperation(pair.getOperation() + " + Коррекция");
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

    public void eject() {
        pairs = null;
    }
}

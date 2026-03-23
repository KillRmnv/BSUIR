/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Алгоритм вычисления целочисленного частного пары 4-разрядных чисел делением без восстановления частичного остатка
Файл реализующий класс инициализирующий конвеер и менеджер с точкой входа в программу
Источники:
(1) Интеграционная платформа

14.03.2026
 */
package com.bsuir;


public class App {
    public static void main(String[] args) throws InterruptedException {
        ConsoleIO consoleIO = new ConsoleIO();
        consoleIO.inputPipelineParams();
        Pipeline pipeline = new Pipeline(Config.amountOfBits);
        PipelineManager pipelineManager = new PipelineManager(pipeline);
        pipelineManager.init();
        pipelineManager.start();
    }
}

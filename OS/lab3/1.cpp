#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <cmath>
#include <chrono>
#include <semaphore.h>
#include <memory>
#include <queue>

// Класс для хранения данных точки
struct Point {
    double x, y;
    Point(double x_val, double y_val) : x(x_val), y(y_val) {}
};

// Потокобезопасная очередь с использованием семафоров
class SafeQueue {
private:
    std::queue<std::shared_ptr<Point>> queue;
    sem_t sem_produce; // Семафор для отслеживания доступности места для добавления
    sem_t sem_consume; // Семафор для отслеживания наличия элементов в очереди

public:
    SafeQueue(size_t max_size) {
        sem_init(&sem_produce, 0, max_size); // Изначально можно добавить max_size элементов
        sem_init(&sem_consume, 0, 0);       // Изначально элементов для потребления нет
    }

    ~SafeQueue() {
        sem_destroy(&sem_produce);
        sem_destroy(&sem_consume);
    }

    void push(std::shared_ptr<Point> point) {
        sem_wait(&sem_produce); // Ожидаем места для добавления
        queue.push(point);
        sem_post(&sem_consume); // Увеличиваем счётчик доступных элементов
    }

    std::shared_ptr<Point> pop() {
        sem_wait(&sem_consume); // Ожидаем, пока элемент будет доступен
        auto point = queue.front();
        queue.pop();
        sem_post(&sem_produce); // Увеличиваем счётчик доступных мест
        return point;
    }
};

SafeQueue queue(10); // Очередь с максимальной вместимостью 10 элементов

// Поток 1: Вычисляет значения функции
void calculate_function() {
    for (double x = 0.0; x <= 10.0; x += 0.1) {
        double y = sin(x); // Здесь можно использовать любую функцию
        auto point = std::make_shared<Point>(x, y);
        queue.push(point); // Добавляем точку в очередь
        std::this_thread::sleep_for(std::chrono::milliseconds(50)); // Задержка для наглядности
    }
}

// Поток 2: Записывает значения в файл
void write_to_file() {
    std::ofstream file("output.txt", std::ios::trunc);
    if (!file.is_open()) {
        std::cerr << "Не удалось открыть файл для записи!" << std::endl;
        return;
    }

    while (true) {
        auto point = queue.pop(); // Получаем точку из очереди
        if (!point) break; // Завершение, если точек больше нет
        file << "x: " << point->x << ", y: " << point->y << std::endl;
    }
    file.close();
}

// Поток 3: Логирует процесс записи
void log_procedure() {
    std::ofstream log("log.txt", std::ios::trunc);
    if (!log.is_open()) {
        std::cerr << "Не удалось открыть файл для логирования!" << std::endl;
        return;
    }

    while (true) {
        auto start_time = std::chrono::system_clock::now();
        auto point = queue.pop(); // Получаем точку из очереди
        if (!point) break; // Завершение, если точек больше нет

        auto write_time = std::chrono::system_clock::now();
        auto duration_ms = std::chrono::duration_cast<std::chrono::milliseconds>(write_time - start_time).count();

        log << "Point (x: " << point->x << ", y: " << point->y
            << ") was processed in " << duration_ms << " ms." << std::endl;
    }
    log.close();
}

// Главная функция
int main() {
    // Очищаем файлы перед началом работы
    std::ofstream("output.txt", std::ios::trunc).close();
    std::ofstream("log.txt", std::ios::trunc).close();

    // Запускаем потоки
    std::thread producer(calculate_function);
    std::thread consumer(write_to_file);
    std::thread logger(log_procedure);

    // Ждём завершения потоков
    producer.join();
    consumer.join();
    logger.join();

    return 0;
}

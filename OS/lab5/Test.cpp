#include <chrono>
#include <iostream>
#include <string>
#include"FileSystem.h"

void performanceTest() {
    using namespace std::chrono;

    FileSystem fs;
    unsigned int memorySize = 1024*1024*900;
    unsigned int clusterSize = 1024*2;

    try {
        // 1. Инициализация файловой системы
        auto start = high_resolution_clock::now();
        fs.allocate_memory(memorySize, clusterSize);
        auto end = high_resolution_clock::now();
        std::cout << "Memory allocation time: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

        // 2. Массовое создание файлов
        start = high_resolution_clock::now();
        for (int i = 0; i < 400; ++i) {
            fs.getCatalog().createFile("file" + std::to_string(i), getCurrentDate(), "rw", 1);
        }
        end = high_resolution_clock::now();
        std::cout << "File creation time for  files: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

       //  3. Запись больших объемов данных
        std::string largeData(1024 * 1024, 'A');
        start = high_resolution_clock::now();
        for (int i = 0; i < 400; ++i) {
            fs.getCatalog().writeFile("file" + std::to_string(i), const_cast<char *>(largeData.c_str()), largeData.size(), true);
        }
        end = high_resolution_clock::now();
        std::cout << "Data writing time for 10 files: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

       //  4. Чтение данных из файлов
        start = high_resolution_clock::now();
        for (int i = 0; i < 400; ++i) {
            fs.getCatalog().readFile("file" + std::to_string(i));
        }
        end = high_resolution_clock::now();
        std::cout << "Data reading time for 10 files: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

        // 5. Копирование файлов
        start = high_resolution_clock::now();
        for (int i = 0; i < 400; ++i) {
            fs.getCatalog().copyFile("file" + std::to_string(i));
        }
        end = high_resolution_clock::now();
        std::cout << "File copy time for 10 files: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

         //6. Удаление файлов
        start = high_resolution_clock::now();
        for (int i = 399; i >-1; --i) {
            fs.getCatalog().deleteFile("file" + std::to_string(i));
        }
        end = high_resolution_clock::now();
        std::cout << "File deletion time for 1000 files: " << duration_cast<milliseconds>(end - start).count() << " ms\n";

    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << '\n';
    }
}

int main() {
  performanceTest();
    FileSystem fs;
    fs.menu.display();
    return 0;
}

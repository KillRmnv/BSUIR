cmake_minimum_required(VERSION 3.10)

# Название проекта
project(MemoryManager)

# Указываем стандарт C
set(CMAKE_C_STANDARD 99)

# Указываем исходные файлы
add_executable(test mmemory.c test.c)

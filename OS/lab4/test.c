#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "mmemory.h"

double measure_time(void (*func)(void *), void *arg) {
    clock_t start = clock();
    func(arg);
    clock_t end = clock();
    return (double)(end - start) / CLOCKS_PER_SEC;
}

typedef struct {
    MemoryManager *manager;
    size_t block_size;
    int num_blocks;
} ExperimentArgs;

void experiment_allocate(void *arg) {
    ExperimentArgs *args = (ExperimentArgs *)arg;
    for (int i = 0; i < args->num_blocks; i++) {
        void *ptr = allocate_memory(args->manager, args->block_size);
        if (ptr == NULL) {
            printf("Allocation failed at block %d\n", i);
        }
    }
}

typedef struct {
    MemoryManager *manager;
    int num_blocks;
    size_t *block_sizes;
} RandomFreeArgs;

void experiment_free_random_blocks(void *arg) {
    RandomFreeArgs *args = (RandomFreeArgs *)arg;

    void **blocks = malloc(args->num_blocks * sizeof(void *));
    if (!blocks) {
        printf("Failed to allocate memory for blocks array\n");
        return;
    }

    // Выделение блоков памяти с произвольными размерами
    for (int i = 0; i < args->num_blocks; i++) {
        blocks[i] = allocate_memory(args->manager, args->block_sizes[i]);
        assert(blocks[i] != NULL); // Убедимся, что память выделена
    }

    // Перемешивание индексов для случайного порядка
    int *indices = malloc(args->num_blocks * sizeof(int));
    if (!indices) {
        printf("Failed to allocate memory for indices array\n");
        free(blocks);
        return;
    }

    for (int i = 0; i < args->num_blocks; i++) {
        indices[i] = i;
    }

    srand((unsigned int)time(NULL)); // Инициализация генератора случайных чисел
    for (int i = 0; i < args->num_blocks; i++) {
        int j = rand() % args->num_blocks;
        int temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }

    // Освобождение блоков памяти в случайном порядке
    for (int i = 0; i < args->num_blocks; i++) {
        int index = indices[i];
        if (blocks[index]) { // Проверяем указатель
            free_memory(args->manager, blocks[index]);
            blocks[index] = NULL; // Помечаем как освобождённый
        }
    }

    printf("All blocks of random sizes freed in random order successfully!\n");

    // Очистка ресурсов
    free(indices);
    free(blocks);
}

void experiment_random_allocate_free(void *arg) {
    RandomFreeArgs *args = (RandomFreeArgs *)arg;

    int half_blocks = args->num_blocks / 2;
    void **blocks = malloc(half_blocks * sizeof(void *));
    if (!blocks) {
        printf("Failed to allocate memory for blocks array\n");
        return;
    }

    // Выделение половины блоков памяти с произвольными размерами
    for (int i = 0; i < half_blocks; i++) {
        blocks[i] = allocate_memory(args->manager, args->block_sizes[i]);
        assert(blocks[i] != NULL); // Убедимся, что память выделена
    }

    // Перемешивание индексов для случайного порядка удаления
    int *indices = malloc(half_blocks * sizeof(int));
    if (!indices) {
        printf("Failed to allocate memory for indices array\n");
        free(blocks);
        return;
    }

    for (int i = 0; i < half_blocks; i++) {
        indices[i] = i;
    }

    srand((unsigned int)time(NULL)); // Инициализация генератора случайных чисел
    for (int i = 0; i < half_blocks; i++) {
        int j = rand() % half_blocks;
        int temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }

    // Освобождение половины блоков в случайном порядке
    for (int i = 0; i < half_blocks / 2; i++) {
        int index = indices[i];
        if (blocks[index]) { // Проверяем указатель
            free_memory(args->manager, blocks[index]);
            blocks[index] = NULL; // Помечаем как освобождённый
        }
    }

    // Выделение второй половины от общего количества блоков
    for (int i = half_blocks; i < args->num_blocks; i++) {
        void *ptr = allocate_memory(args->manager, args->block_sizes[i]);
        assert(ptr != NULL); // Убедимся, что память выделена
    }

    printf("Random allocate, free, and reallocate experiment completed successfully!\n");

    // Очистка ресурсов
    free(indices);
    free(blocks);
}

void experiment_write(void *arg) {
    ExperimentArgs *args = (ExperimentArgs *)arg;
    char data[args->block_size];
    memset(data, 'A', args->block_size);

    for (int i = 0; i < args->num_blocks; i++) {
        void *block = allocate_memory(args->manager, args->block_size);
        if (block != NULL) {
            write_memory(args->manager, block, data, args->block_size);
        }
    }
}

void experiment_read(void *arg) {
    ExperimentArgs *args = (ExperimentArgs *)arg;
    char buffer[args->block_size];
    memset(buffer, 0, args->block_size);

    void **blocks = malloc(args->num_blocks * sizeof(void *));
    for (int i = 0; i < args->num_blocks; i++) {
        blocks[i] = allocate_memory(args->manager, args->block_size);
        if (blocks[i] != NULL) {
            write_memory(args->manager, blocks[i], "TestData", 8);
        }
    }

    for (int i = 0; i < args->num_blocks; i++) {
        if (blocks[i] != NULL) {
            read_memory(args->manager, blocks[i], buffer, args->block_size);
        }
    }

    free(blocks);
}

void experiment_free(void *arg) {
    ExperimentArgs *args = (ExperimentArgs *)arg;

    void **blocks = malloc(args->num_blocks * sizeof(void *));
    for (int i = 0; i < args->num_blocks; i++) {
        blocks[i] = allocate_memory(args->manager, args->block_size);
    }

    for (int i = 0; i < args->num_blocks; i++) {
        if (blocks[i] != NULL) {
            free_memory(args->manager, blocks[i]);
        }
    }

    free(blocks);
}

void run_experiment() {
    MemoryManager manager;
    size_t memory_size = 1024 * 1024; // 1 MB
    memory_manager_init(&manager, memory_size);

    size_t block_size = 128;
    int num_blocks = 1000;

    ExperimentArgs args = {&manager, block_size, num_blocks};

    double time_alloc = measure_time(experiment_allocate, &args);
    printf("Time for allocation: %f seconds\n", time_alloc);

    double time_write = measure_time(experiment_write, &args);
    printf("Time for write: %f seconds\n", time_write);

    double time_read = measure_time(experiment_read, &args);
    printf("Time for read: %f seconds\n", time_read);

    double time_free = measure_time(experiment_free, &args);
    printf("Time for free: %f seconds\n", time_free);

    free(manager.memory);
    free(manager.blocks);
     memory_size = 1024 * 1024*5;
    memory_manager_init(&manager, memory_size);

     block_size = 128;
     num_blocks = 5000;

    ExperimentArgs args1 = {&manager, block_size, num_blocks};

     time_alloc = measure_time(experiment_allocate, &args1);
    printf("Time for allocation: %f seconds\n", time_alloc);

     time_write = measure_time(experiment_write, &args1);
    printf("Time for write: %f seconds\n", time_write);

     time_read = measure_time(experiment_read, &args1);
    printf("Time for read: %f seconds\n", time_read);

     time_free = measure_time(experiment_free, &args1);
    printf("Time for free: %f seconds\n", time_free);

    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024*10;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 10000;

    ExperimentArgs args2 = {&manager, block_size, num_blocks};

    time_alloc = measure_time(experiment_allocate, &args2);
    printf("Time for allocation: %f seconds\n", time_alloc);

    time_write = measure_time(experiment_write, &args2);
    printf("Time for write: %f seconds\n", time_write);

    time_read = measure_time(experiment_read, &args2);
    printf("Time for read: %f seconds\n", time_read);

    time_free = measure_time(experiment_free, &args2);
    printf("Time for free: %f seconds\n", time_free);

    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024*20;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 20000;

    ExperimentArgs args3 = {&manager, block_size, num_blocks};

    time_alloc = measure_time(experiment_allocate, &args3);
    printf("Time for allocation: %f seconds\n", time_alloc);

    time_write = measure_time(experiment_write, &args3);
    printf("Time for write: %f seconds\n", time_write);

    time_read = measure_time(experiment_read, &args3);
    printf("Time for read: %f seconds\n", time_read);

    time_free = measure_time(experiment_free, &args3);
    printf("Time for free: %f seconds\n", time_free);

    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024*50;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 50000;

    ExperimentArgs args4 = {&manager, block_size, num_blocks};

    time_alloc = measure_time(experiment_allocate, &args4);
    printf("Time for allocation: %f seconds\n", time_alloc);

    time_write = measure_time(experiment_write, &args4);
    printf("Time for write: %f seconds\n", time_write);

    time_read = measure_time(experiment_read, &args4);
    printf("Time for read: %f seconds\n", time_read);

    time_free = measure_time(experiment_free, &args4);
    printf("Time for free: %f seconds\n", time_free);

    free(manager.memory);
    free(manager.blocks);





     memory_size = 1024 * 1024 * 5;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 5000;

    RandomFreeArgs random_args1 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args1.block_sizes[i] = rand() % 256 + 1;
    }

    time_free = measure_time(experiment_free_random_blocks, &random_args1);
    printf("Time for free random (1): %f seconds\n", time_free);

    free(random_args1.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 10; // 10 MB
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 10000;

    RandomFreeArgs random_args2 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args2.block_sizes[i] = rand() % 512 + 1;
    }

    time_free = measure_time(experiment_free_random_blocks, &random_args2);
    printf("Time for free random (2): %f seconds\n", time_free);

    free(random_args2.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 20;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 20000;

    RandomFreeArgs random_args3 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args3.block_sizes[i] = rand() % 1024 + 1;
    }

    time_free = measure_time(experiment_free_random_blocks, &random_args3);
    printf("Time for free random (3): %f seconds\n", time_free);

    free(random_args3.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 50;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 50000;

    RandomFreeArgs random_args4 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args4.block_sizes[i] = rand() % 2048 + 1;
    }

    time_free = measure_time(experiment_free_random_blocks, &random_args4);
    printf("Time for free random (4): %f seconds\n", time_free);

    free(random_args4.block_sizes);
    free(manager.memory);
    free(manager.blocks);


     memory_size = 1024 * 1024;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 1000;

    RandomFreeArgs random_args0 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args0.block_sizes[i] = rand() % 128 + 1;
    }

    time_free = measure_time(experiment_random_allocate_free, &random_args0);
    printf("Time for random allocate and free (1 MB): %f seconds\n", time_free);

    free(random_args0.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 5;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 5000;

    RandomFreeArgs random_args12 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args12.block_sizes[i] = rand() % 256 + 1;
    }

    time_free = measure_time(experiment_random_allocate_free, &random_args12);
    printf("Time for random allocate and free (5 MB): %f seconds\n", time_free);

    free(random_args12.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 10; // 10 MB
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 10000;

    RandomFreeArgs random_args22 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args22.block_sizes[i] = rand() % 512 + 1;
    }

    time_free = measure_time(experiment_random_allocate_free, &random_args22);
    printf("Time for random allocate and free (10 MB): %f seconds\n", time_free);

    free(random_args22.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 20;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 20000;

    RandomFreeArgs random_args32 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args32.block_sizes[i] = rand() % 1024 + 1;
    }

    time_free = measure_time(experiment_random_allocate_free, &random_args32);
    printf("Time for random allocate and free (20 MB): %f seconds\n", time_free);

    free(random_args32.block_sizes);
    free(manager.memory);
    free(manager.blocks);

    memory_size = 1024 * 1024 * 50;
    memory_manager_init(&manager, memory_size);

    block_size = 128;
    num_blocks = 50000;

    RandomFreeArgs random_args42 = {
        .manager = &manager,
        .num_blocks = num_blocks,
        .block_sizes = malloc(num_blocks * sizeof(size_t))
    };
    for (int i = 0; i < num_blocks; i++) {
        random_args42.block_sizes[i] = rand() % 2048 + 1;
    }

    time_free = measure_time(experiment_random_allocate_free, &random_args42);
    printf("Time for random allocate and free (50 MB): %f seconds\n", time_free);

    free(random_args4.block_sizes);
    free(manager.memory);
    free(manager.blocks);

}

void test_memory_manager_init() {
    MemoryManager manager;
    size_t size = 1024;
    memory_manager_init(&manager, size);

    assert(manager.total_size == size);
    assert(manager.memory != NULL);
    assert(manager.blocks != NULL);
    assert(manager.allocated_memory == 0);

    printf("test_memory_manager_init passed!\n");
}

void test_allocate_memory() {
    MemoryManager manager;
    memory_manager_init(&manager, 1024);

    void *ptr1 = allocate_memory(&manager, 100);
    assert(ptr1 != NULL);
    assert(manager.allocated_memory == 100);

    void *ptr2 = allocate_memory(&manager, 200);
    assert(ptr2 != NULL);
    assert(manager.allocated_memory == 300);

    void *ptr3 = allocate_memory(&manager, 800);
    assert(ptr3 == NULL);

    printf("test_allocate_memory passed!\n");
}

void test_free_memory() {
    MemoryManager * manager= malloc(sizeof(MemoryManager));;
    memory_manager_init(manager, 1024);

    void *ptr1 = allocate_memory(manager, 100);
    void *ptr2 = allocate_memory(manager, 200);

    free_memory(manager, ptr2);
    assert(manager->blocks->next->is_free==true);

    free_memory(manager, ptr1);
    assert(manager->blocks->next->is_free==true);

    printf("test_free_memory passed!\n");
}

void test_write_and_read_memory() {
    MemoryManager manager;
    memory_manager_init(&manager, 1024);

    char data[] = "Hello, Memory!";
    void *ptr = allocate_memory(&manager, sizeof(data));
    assert(write_memory(&manager, ptr, data, sizeof(data)) == true);

    char buffer[50];
    void *read_ptr = read_memory(&manager, ptr, buffer, sizeof(data));
    assert(read_ptr != NULL);
    assert(strcmp(buffer, data) == 0);

    printf("test_write_and_read_memory passed!\n");
}

int main() {
    test_memory_manager_init();
    test_allocate_memory();
    test_free_memory();
    test_write_and_read_memory();
    run_experiment();

    printf("All tests passed!\n");
    return 0;
}
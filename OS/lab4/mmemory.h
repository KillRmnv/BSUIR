
#ifndef MMEMORY_H
#define MMEMORY_H
#include <string.h>
#include <stdbool.h>

typedef struct MemoryBlock {
    size_t start;
    size_t size;
    struct MemoryBlock *next;
    bool is_free;
} MemoryBlock;

typedef struct {
    size_t total_size;
    void *memory;
    MemoryBlock *blocks;
    size_t allocated_memory;
} MemoryManager;

void memory_manager_init(MemoryManager *manager, size_t size);
void *allocate_memory(MemoryManager *manager, size_t size);
void free_memory(MemoryManager *manager, const void *ptr);
void* read_memory(const MemoryManager *manager, const void *ptr, void *buffer, size_t size);
bool write_memory(MemoryManager *manager, void *ptr, const void *data, size_t size);
void merge_two_blocks(MemoryBlock *previous_block, MemoryBlock *onTop);

#endif

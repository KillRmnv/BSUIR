
#include "mmemory.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void merge_two_blocks(MemoryBlock *previous_block, MemoryBlock *onTop) {

    previous_block->start = onTop->start;
    previous_block->size += onTop->size;
    previous_block->next=previous_block->next->next;

}
void memory_manager_init(MemoryManager *manager, size_t size) {

    manager->total_size = size;
    manager->memory = malloc(size);
    manager->blocks = malloc(sizeof(MemoryBlock));
    manager->blocks->size=0;
    manager->blocks->start=0;
    manager->blocks->is_free=true;
    manager->blocks->next=NULL;
    manager->allocated_memory=0;

}

void *allocate_memory(MemoryManager *manager, size_t size) {

    if (manager->total_size - manager->allocated_memory >= size) {

        MemoryBlock *new_block = malloc(sizeof(MemoryBlock));
        manager->blocks->size = size;
        manager->blocks->is_free=false;
        new_block->size = 0;
        new_block->next = manager->blocks;
        new_block->is_free=true;
        new_block->start = manager->blocks->start+size;
        manager->blocks = new_block;
        manager->allocated_memory += size;
        return manager->memory + (manager->allocated_memory - size);

    }else {

        MemoryBlock* current_block = manager->blocks->next;

        while (current_block ->next!= NULL ) {

            if (current_block->size >= size&&current_block->is_free) {
                MemoryBlock * new_one=malloc(sizeof(MemoryBlock));
                new_one->size = size;
                new_one->is_free=false;
                new_one->start = current_block->start;
                new_one->next = current_block->next;
                current_block->next = new_one;
                current_block->start = new_one->start+size;
                current_block->size-=size;
                return manager->memory+new_one->start;


            }

            current_block = current_block->next;

        }

            printf("No free memory\n");

    }

    return NULL;
}

void free_memory(MemoryManager *manager, const void *ptr) {

    if (ptr == NULL||manager==NULL) {

        printf("Pointer is NULL, nothing to free.\n");
        return;

    }

    MemoryBlock *onTop = manager->blocks->next;
    MemoryBlock * previous_block = manager->blocks;

    while (manager->memory + onTop->start != ptr && onTop->next != NULL) {

        onTop = onTop->next;
        previous_block = previous_block->next;

    }

    if (manager->memory + onTop->start == ptr) {

        onTop->is_free=true;
        if (previous_block->is_free&&previous_block!=manager->blocks) {

           merge_two_blocks(previous_block, onTop);
            free(onTop);
            onTop=previous_block->next;

            while (onTop != NULL&&onTop->is_free) {

                merge_two_blocks(previous_block, onTop);
                free(onTop);
                onTop=previous_block->next;

            }

        }

    } else {

        printf("Memory block not found\n");

    }
}

void *read_memory(const MemoryManager *manager, const void *ptr, void *buffer, const size_t size) {

    if (ptr == NULL)
        return NULL;

    MemoryBlock *onTop = manager->blocks;
    unsigned int reading_memory = onTop->next->size;

    while (manager->memory + (manager->allocated_memory - reading_memory) != ptr && onTop->next != NULL) {

        onTop = onTop->next;
        reading_memory += onTop->next->size;

    }

    if (manager->memory + (manager->allocated_memory - reading_memory) == ptr) {

        if (onTop->next->size < size)
            return NULL;

    }else{

        printf("Memory block not found\n");
        return NULL;

    }

    if (buffer == NULL)
        buffer = malloc(size);

    memcpy(buffer, ptr, size);
    return buffer;

}

bool write_memory(MemoryManager *manager, void *ptr, const void *data, const size_t size) {

    if (data == NULL)
        return false;

    if (ptr == NULL) {

        ptr = allocate_memory(manager, size);
        if (ptr == NULL) return false;

    }

    memcpy(ptr, data, size);
    return true;

}
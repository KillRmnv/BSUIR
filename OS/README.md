# Operating Systems Laboratory Works

This repository contains the laboratory works for the Operating Systems course. Each lab focuses on different aspects of operating systems concepts and implementations.

## Lab 1: File Search and Filtering
**File:** `lab1/lab1.sh`

A bash script that searches for files in a specified directory based on:
- File size range (minimum and maximum size)
- File owner username
- Outputs matching files to a specified file with details including path, filename, and size

**Key Concepts:**
- Bash scripting
- File system traversal using `find`
- File attribute extraction using `stat`
- Conditional filtering based on file properties
- Output redirection and formatting

## Lab 2: Process Management
**File:** `lab2/lab2.cpp`

Demonstrates process creation, management, and inter-process communication using:
- `fork()` system call to create child processes
- Process identification (PID, PPID)
- Process waiting mechanisms
- Execution of system commands (`ps`) using `execl`

**Key Concepts:**
- Process creation and lifecycle
- Parent-child process relationships
- Process synchronization with `waitpid`
- Executing programs from within a process
- Basic inter-process communication concepts

## Lab 3: Multithreading and Synchronization
**File:** `lab3/1.cpp`

Implements a producer-consumer pattern using C++ threads and semaphores for synchronization:
- Producer thread calculates mathematical function values (sin(x))
- Consumer thread writes results to a file
- Logger thread monitors and logs processing times
- Thread-safe queue implementation using semaphores

**Key Concepts:**
- Multithreading with std::thread
- Thread synchronization using semaphores
- Producer-consumer problem solution
- Shared resource protection
- Inter-thread communication

## Lab 4: Custom Memory Manager
**Files:** 
- `lab4/mmemory.h` - Header file with data structures and function declarations
- `lab4/mmemory.c` - Implementation of memory manager functions
- `lab4/test.c` - Comprehensive test suite and performance experiments

Implements a custom memory manager with:
- Dynamic memory allocation and deallocation
- Memory block tracking and management
- Memory coalescing (merging adjacent free blocks)
- Read and write operations on managed memory
- Performance testing under various conditions

**Key Concepts:**
- Manual memory management
- Free list implementation
- Memory fragmentation and coalescing
- Allocation strategies (first-fit)
- Memory safety and boundary checking
- Performance measurement and analysis

## Lab 5: File System Simulation
**Files:**
- `lab5/main.cpp` - Main implementation with menu interface
- `lab5/FileSystem.h` - Header file with class declarations
- `lab5/Test.cpp` - Additional test functionality

Simulates a file system with FAT (File Allocation Table) concepts:
- Cluster-based storage allocation
- File creation, deletion, reading, writing, and copying
- File attributes (read/write permissions)
- Cluster table management
- Memory allocation for storage space
- Menu-driven interface for file system operations

**Key Concepts:**
- File allocation table (FAT) simulation
- Cluster-based storage management
- File metadata handling (creation date, permissions)
- Sequential and random file access
- Space allocation and deallocation strategies
- File system integrity maintenance

## Building and Running

Each lab can be compiled and run individually. Most labs use standard C++ compilation:

```bash
# For C++ labs
g++ -std=c++11 -pthread labX/*.cpp -o labX
./labX

# For C labs
gcc labX/*.c -o labX
./labX
```

Refer to individual lab directories for specific compilation instructions if needed.

## Learning Outcomes

Through these laboratory works, students gain practical experience with:
1. System-level programming in bash and C/C++
2. Process and thread management
3. Synchronization primitives and inter-process communication
4. Memory management techniques and challenges
5. File system organization and implementation details
6. Performance analysis and optimization considerations
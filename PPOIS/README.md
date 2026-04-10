# PPOIS Course Repository

This repository contains educational materials, lab works, and course projects for the PPOIS (Object-Oriented Programming in Software Systems) course.

## Contents

### Lecture Materials
- Basic OOP concepts
- Abstract data types
- Memory management
- Modularity
- Fault tolerance in software systems
- Generic programming
- Structure of standard class library
- Functional programming style
- Multitasking programming

### Laboratory Works

#### Lab 1: Set Implementation in C++
Implementation of set operations with custom Element and Set classes.
- Element class definition
- Set class with operations (+, *, -, etc.) and power set functionality
- Supporting files: input handling, UI, test files

#### Lab 2: Document Management System in C++
C++ application for managing documents with employee roles and workflows.
- Employee hierarchy with different roles (Administrator, Bookkeeper, Lawyer, etc.)
- Document workflow management
- JSON serialization/deserialization
- Comprehensive test suite

#### Lab 3: Airport Simulation in C++
Object-oriented simulation of airport operations.
- Classes: Aircraft, Airline, Airport, Flight, Passenger, Baggage, etc.
- Various airport zones and services (Security, Maintenance, Gate control)
- Time management with SysDate class

#### Lab 4: Graph Implementation in C++
Generic graph implementation with iterator patterns.
- Graph class with adjacency list representation
- VertexIterator and EdgeIncedentIterator for traversal
- GraphTest.cpp for verification


#### PPOIS 1: Law Registry System (Java)
State machine-based application for managing legal cases and investigations.
- Built with Maven
- Uses JSON for data persistence
- Implements state machine pattern for different departments:
  - Control Centre
  - Enforcement Department
  - HR Department
  - Investigation Department
  - Police
  - Public Safety Department
- Features: Case management, suspect tracking, law registry, department workflows

#### PPOIS 2: Customer Processing System (JavaFX)
Desktop application for customer data management.
- Built with JavaFX for GUI
- Supports multiple data sources: SQLite, XML
- MVC architecture with controllers for:
  - Adding customers
  - Deleting customers
  - Searching customers
  - Main application control
- Features: Customer search, data validation, multiple storage backends

## Technologies Used
- C++: Labs 1-4 (Modern C++ with STL)
- Java: PPOIS 1 and PPOIS 2 (Core Java)
- JavaFX: PPOIS 2 (GUI framework)
- Maven: Build automation for Java projects
- JSON: Data persistence in PPOIS 1
- SQLite/XML: Data storage options in PPOIS 2
- nlohmann/json: JSON library for C++ in Lab 2

## Building and Running

### C++ Labs
Each lab can be compiled with a modern C++ compiler:
```bash
g++ -std=c++17 -o labX_source labX_source.cpp -lnlohmann_json  # For Lab 2
```

### Java Projects
#### PPOIS 1
```bash
cd PPOIS1
mvn clean package
java -jar target/ppois1.jar
```

#### PPOIS 2
```bash
cd PPOIS2
mvn clean package
java -jar target/ppois2.jar
```

## Learning Objectives Demonstrated
- Object-oriented design principles (encapsulation, inheritance, polymorphism)
- Data structures and algorithms
- Design patterns (State Machine, MVC, Iterator)
- File I/O and data persistence
- Multi-language software development
- Testing methodologies
- GUI development (JavaFX)
- Database integration (SQLite)

## Notes
All code is developed for educational purposes as part of the PPOIS course curriculum.
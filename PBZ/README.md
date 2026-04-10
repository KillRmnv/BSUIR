# PBZ Academic Projects

This repository contains three distinct academic projects completed as part of the PBZ coursework, covering database design, software engineering, and semantic web technologies.

## Project Structure

```
PBZ/
├── 1/                    # Database Design Project
├── PBZ2/                 # Library Management System
└── PBZ3/                 # Ontology Development Project
```

---

## 1. Database Design Project (Directory "1")

This project focuses on relational database design and implementation using SQL. It implements a classic supplier-parts-projects database schema.

### Contents
- `creation.sql`: SQL script for creating database schema and inserting sample data
- `queries.sql`: SQL queries for data retrieval and manipulation
- `creation`: Text version of the database schema
- `queries`: Text version of SQL queries
- `1.docx`: Detailed documentation (likely in Russian)

### Database Schema
The database consists of four tables:

1. **Поставщики S (Suppliers S)**
   - П# (Supplier ID) - Primary Key
   - Имя П (Supplier Name)
   - Статус (Status)
   - Город (City)

2. **Детали P (Parts P)**
   - Д# (Part ID) - Primary Key
   - Имя Д (Part Name)
   - Цвет (Color)
   - Размер (Size)
   - Город (City)

3. **Проекты J (Projects J)**
   - ПР# (Project ID) - Primary Key
   - Имя ПР (Project Name)
   - Город (City)

4. **Поставки SPJ (Supplies SPJ)**
   - П# (Supplier ID) - Foreign Key referencing Поставщики S
   - Д# (Part ID) - Foreign Key referencing Детали P
   - ПР# (Project ID) - Foreign Key referencing Проекты J
   - S (Quantity)

### Sample Data
The database includes sample data for:
- 5 suppliers (П1-П5)
- 6 parts (Д1-Д6)
- 8 projects (ПР1-ПР8)
- Various supply relationships with quantities

---

## PBZ2. Library Management System

This project implements a library management system using Java and Maven, following object-oriented design principles.

### Contents
- `pom.xml`: Maven project configuration
- `src/`: Source code directory
- `db2.md`: Database design documentation
- `.idea/`: IntelliJ IDEA configuration
- `.gitignore`: Git ignore rules

### Database Schema (from source code)

Based on the SQL schema provided in the source code, the database includes:

1. **Departments**
   - department_id - serial (Primary Key)
   - department_name - varchar(64) (Unique, Not Null)

2. **PublicationTypes**
   - type_id - serial (Primary Key)
   - type_name - varchar(64) (Unique, Not Null)

3. **Frequencies**
   - freq_id - SERIAL (Primary Key)
   - freq_name - VARCHAR(30) (Unique, Not Null)
   - CHECK constraint: freq_name IN ('ежедневно', 'еженедельно', 'ежемесячно', 'ежеквартально', 'раз в полгода')

4. **Employees**
   - employee_id - serial (Primary Key)
   - second_name - varchar(64) (Not Null)
   - first_name - varchar(64) (Not Null)
   - third_name - varchar(64) (Not Null)
   - position - varchar(64) (Not Null)
   - department_id - integer (References Departments(department_id), ON DELETE SET NULL)

5. **Printings**
   - name - varchar(64) (Not Null)
   - index - integer (Primary Key, Unique, CHECK: index > 0)
   - freq_id - integer (Not Null, References Frequencies(freq_id), ON DELETE SET NULL)
   - type_id - integer (Default 1, References PublicationTypes(type_id), ON DELETE SET DEFAULT)

6. **SubsPeriods**
   - freq_id - SERIAL (Primary Key)
   - freq_name - VARCHAR(30) (Unique, Not Null)
   - CHECK constraint: freq_name IN ('год', 'полгода')

7. **Subs**
   - id - serial (Primary Key)
   - index_printing - integer (References Printings(index), ON DELETE CASCADE)
   - employee_id - integer (References Employees(employee_id), ON DELETE CASCADE)
   - date_beg - date (Not Null)
   - date_end - date (Not Null)
   - period - integer (Default 1, References SubsPeriods(freq_id), ON DELETE SET DEFAULT, Not Null)
   - cost - integer (Check: cost > 0, Not Null)

8. **Circulation**
   - id - serial (Primary Key)
   - pub_id - integer (References Printings(index), ON DELETE CASCADE)
   - amount - integer (Check: amount > 0)
   - allocated_amount - integer (Check: allocated_amount > -1, Default 0)
   - num_of_pub - integer (Check: num_of_pub > 0)

9. **HistoryStates**
   - state_id - serial (Primary Key)
   - state_name - varchar(128) (Not Null)
   - Initial values: 'Выписано', 'Получено'

10. **History**
    - id - serial (Primary Key)
    - date_hist - date
    - subscription_id - integer (References Subs(id))
    - num_pub - integer (References Circulation(num_of_pub), Check: num_pub > 0)
    - state - integer (References HistoryStates(state_id), ON DELETE RESTRICT)
    - Additional constraints:
      - fk_num_pub: foreign key (num_pub) references Circulation(id) ON DELETE NO ACTION
      - chck_num_of_printing: check (num_pub > 0)

11. **DeliveryType**
    - id - serial (Primary Key)
    - type_d - varchar(128)

12. **delivery**
    - delivery_id - serial (Primary Key)
    - type_d - integer (Default 1, References DeliveryType(id), ON DELETE SET DEFAULT)
    - address - varchar(128) (Not Null)
    - hist_id - integer (References History(id), ON DELETE CASCADE)
    - expected_date - date

13. **Organization**
    - id - serial (Primary Key)
    - name - varchar(64)
    - base_address_for_delivery - varchar(64)
    - type_of_delivery - integer (References DeliveryType(id))

### CRUD Implementation

The project implements a generic CRUD repository pattern using PostgreSQL stored procedures:

1. **Generic Repository Class** (`PostgreSQLRepository`)
   - Implements `DBInterface`, `DBMainMenuInterface`, and `DBReferenceData` interfaces
   - Uses dependency injection for `DataSource` via constructor
   - Marked as `@Singleton` for dependency injection

2. **Dynamic SQL Generation**
   - Uses stored procedures for all CRUD operations
   - Function names determined dynamically via `get_function_name()` method
   - Calls stored procedure named `[ClassName]_[operation]` where operation is c(rudate), r(ead), u(pdate), d(elete)

3. **Flexible Search (Unlimited Parameters)**
   - The `find()` method accepts a `List<Object> template_entity` and `Class clazz`
   - Each object in the list represents a parameter for the stored procedure
   - Number of parameters is not fixed - depends on the entity being searched
   - Example usage: `repository.find(Arrays.asList("value1", 123, true), MyEntity.class)`

4. **Create Operation** (`save()`)
   - Calls stored procedure: `CALL [ClassName]_c`
   - Parameters passed as list elements to prepared statement
   - Returns boolean indicating success

5. **Read Operation** (`find()`)
   - Calls stored procedure: `SELECT * FROM [ClassName]_r`
   - Parameters passed as list elements to prepared statement
   - Returns `List<Map<String, Object>>` where each map represents a row
   - Column names mapped from ResultSetMetaData

6. **Update Operation** (`update()`)
   - Calls stored procedure: `CALL [ClassName]_u`
   - Parameters passed as list elements to prepared statement
   - Returns integer (typically rows affected)

7. **Delete Operation** (`delete()`)
   - Calls stored procedure: `CALL [ClassName]_d`
   - Parameters passed as list elements to prepared statement
   - No return value (void)

8. **Specialized Queries**
   - `findPrintingsByStateAndType()` - Custom query with two string parameters
   - `printingsForYear()` - Custom query with integer year parameter
   - `unrecievedPrintingsForTwoMonths()` - Parameterless custom query
   - `employeesByMonthAndDepartment()` - Custom query with three parameters (int, date, int)

9. **Utility Methods**
   - `getMaps()` - Converts ResultSet to List of Maps
   - `findAll()` - Loads all records from a reference table

### Technologies Used
- Java
- Maven
- PostgreSQL
- Stored Procedures for business logic
- Dependency Injection (Jakarta Inject)
- JDBC for database access

---

## PBZ3. Ontology Development Project

This project involves creating and querying ontologies using semantic web technologies (OWL/RDF).

### Contents
- OWL/TLL files: Ontology definitions
  - `EDAM.owl`: Base ontology (3.3MB)
  - `ontologiev3.owl`: Custom ontology
  - Various `.ttl` files: Turtle format ontologies
- SPARQL queries: `quriesToMyOntolpgie.sparql`
- Ontology diagrams: 
  - `classHierarchy.png`
  - `graph.png`
- Data files:
  - `123.ttl`, `ALLL.owx`, `ALLL.ttl`, `ModSci.ttl`: Ontology instances
  - `catalog-v001.xml`: XML catalog
- `my-app/`: Web application for ontology visualization/interaction
- `graph`: Empty directory (possibly for generated graphs)
- `.zed/`: Zed editor configuration

### Ontology Features
The ontology appears to model technical sciences disciplines with classes for:
- TheoreticalDiscipline
- AppliedDiscipline
- MaterialObject
- TechnologicalEra
- SystemObject
- TechnicalDevice

Properties include:
- hasName
- mathematicalComplexity
- foundationYear
- industryRelevance
- practicalApplication
- usesMethod
- methodAccuracy
- startYear, endYear
- systemComplexity
- integrationLevel
- powerConsumption
- partOfSystem

### SPARQL Queries
The project includes SPARQL queries for:
1. Retrieving theoretical disciplines ordered by foundation year
2. Finding applied disciplines with high/critical industry relevance
3. Mapping materials to methods with accuracy metrics
4. Counting disciplines per technological era
5. Querying complex systems and their devices with filtering capabilities

---

## Technologies Used

### Project 1
- SQL (PostgreSQL syntax)
- Relational Database Design

### PBZ2
- Java
- Maven
- PostgreSQL
- Stored Procedures
- Dependency Injection (Jakarta Inject)
- JDBC

### PBZ3
- OWL/RDF
- SPARQL
- XML
- Semantic Web Technologies
- Possibly Java-based web application (my-app/)

## Setup Instructions

Each project has its own setup requirements:

### Project 1
1. Load `creation.sql` into PostgreSQL database
2. Run queries from `queries.sql` as needed

### PBZ2
1. Ensure Java JDK is installed
2. Configure PostgreSQL database with the schema provided above
3. Run `mvn clean install` to build
4. Follow any specific instructions in source code

### PBZ3
1. Use ontology editor (Protégé, etc.) to view/modify `.owl` and `.ttl` files
2. Load data into SPARQL endpoint for querying
3. For web application: check `my-app/` directory for specific instructions


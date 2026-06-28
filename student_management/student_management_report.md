# Design and Implementation of a Menu-Driven Student Record Management System with Hybrid CSV-JSON Data Persistence and Transactional Exception Safety

**Abstract**—This report presents the design, architectural patterns, and testing results of a Student Record Management System implemented as a command-line interface (CLI) Python application. To satisfy persistence requirements and demonstrate hybrid database structures, the system separates student data into core identification fields stored in a Comma-Separated Values (CSV) format and extended demographic details stored in a JavaScript Object Notation (JSON) format. Data integrity across these heterogeneous file formats is maintained via a custom transactional rollback architecture. In addition, the application incorporates strict regular expression-based input validation, comprehensive audit logging of all user operations and errors, and a custom exception hierarchy. Empirical evaluation confirms that the system maintains data consistency under normal operation, gracefully handles boundary states, and rolls back cleanly when file writing operations fail.

**Keywords**—CSV, JSON, Python OOP, input validation, transaction rollback, exception handling, system logging, audit trails, CLI design.

---

## I. Introduction

Modern information systems rely on relational or document-oriented databases to guarantee data persistence, integrity, and query efficiency. In academic and enterprise settings, record management applications must offer high reliability, strict input formatting, and thorough event logging.

This project implements a lightweight **Student Record Management System** in Python. The system functions as a menu-driven program that persists records across two independent flat-file structures:
1. A tabular **CSV database** containing core fields: `registration_number`, `name`, and `email`.
2. A document-oriented **JSON database** storing additional, dynamic fields: `address`, `contact`, and `program`, mapped via the registration number.

Crucially, because file operations do not naturally support ACID (Atomicity, Consistency, Isolation, Durability) properties, this application implements a custom software-level transactional framework. If write operations fail in either storage format, the program automatically executes a fallback write operation to restore the databases to their pre-operation states.

---

## II. System Architecture & Program Design

The system follows a modular architecture separating the Presentation Layer (CLI Menu), Business Logic Layer (Validators and CRUD operations), and Data Persistence Layer (CSV and JSON interfaces), as modeled in Fig. 1.

```
       +-----------------------------------------------+
       |             Presentation Layer (CLI)          |
       |  (Menu Selection Loop, Dynamic Print Grids)  |
       +-----------------------+-----------------------+
                               |
                               v
       +-----------------------------------------------+
       |             Business Logic Layer              |
       | - Regex Validators   - Custom Exceptions      |
       | - Logging Utilities  - Transaction Controller |
       +-----------------------+-----------------------+
                               |
                               v
       +-----------------------------------------------+
       |             Data Persistence Layer            |
       |  - csv.DictWriter    - json.dump (JSON)       |
       |  - csv.DictReader    - json.load (JSON)       |
       +-----------------------+-----------------------+
```
*Fig. 1. Three-tier application logic diagram.*

### A. Persistent Storage Schema
The database files are linked relationally through a primary key constraint enforced on the registration number. The structural schemas are detailed below:

*   **Core Records (`students.csv`)**:
    *   `registration_number` (String, Primary Key): Unique alphanumeric ID.
    *   `name` (String): Full alphabetical student name.
    *   `email` (String): Unique validated email address.
*   **Extended Records (`students.json`)**:
    *   Outer Key: `registration_number`
    *   Properties: `address` (String), `contact` (String), `program` (String).

### B. Directory Structure
The files are colocated under a dedicated directory to facilitate portability and isolation:
*   `student_management/`
    *   `student_management.py` (Core logic and entry point)
    *   `students.csv` (Core tabular persistence)
    *   `students.json` (Extended document persistence)
    *   `student_system.log` (Chronological runtime audit trail)
    *   `student_management_report.md` (IEEE System Documentation)

---

## III. Core Operations & Key Functions

The program logic is encapsulated in several key routines:

### A. Input Verification Mechanics
Strict verification routines inspect input strings before operations are allowed to alter database objects. Regular expressions are compiled to ensure maximum efficiency:

1.  **Registration Number Validation**:
    $$\text{Pattern: } \texttt{`^[a-zA-Z0-9\-_]+$`}$$
    Restricts IDs to letters, numbers, hyphens, and underscores to prevent injection risks and command line parameter issues.
2.  **Full Name Validation**:
    $$\text{Pattern: } \texttt{`^[a-zA-Z\s\.\-]+$`}$$
    Allows spaces, dots, and hyphens but restricts numerical digits or symbols.
3.  **Email Address Validation**:
    $$\text{Pattern: } \texttt{`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`}$$
    Enforces a strict email domain syntax structure.
4.  **Contact Number Validation**:
    $$\text{Pattern: } \texttt{`^\+?[0-9\s\-()]{7,20}$`}$$
    Validates numbers with standard optional country prefixes, spaces, brackets, or dashes.

### B. Database Access and Operations (CRUD)
The logical transactions are implemented via the following programmatic operations:

*   `load_csv_records()` / `load_json_records()`: Read raw data from disk into memory lists and dictionaries. In case of missing files, they automatically initialize empty baseline objects.
*   `add_student()`: Validates inputs, checks for uniqueness in memory, and writes to both endpoints. If either write fails, it falls back to backing copies.
*   `view_all_students()`: Aggregates records from both endpoints using a relational left-outer join on the key `registration_number`. Outputs a clean ASCII table with automatic column width constraints.
*   `search_student()`: Queries database lists, matching the target ID and showing details on the screen.
*   `update_student()`: Reads records, provides inline editing by showing current fields as defaults, updates changed fields, validates new inputs, and saves files.
*   `delete_student()`: Prompts for double confirmation and removes records from both files.

---

## IV. Exception Handling & Security Controls

A key requirement of this system is robust recovery from standard and runtime errors.

### A. Exception Hierarchy
To distinguish user inputs from file IO failures, we construct a hierarchy of custom exceptions inheriting from Python's base `Exception` class, shown in Fig. 2.

```
                  +--------------------------+
                  |        Exception         |
                  +-------------+------------+
                                |
                                v
                  +--------------------------+
                  |  StudentManagementError  |
                  +-------------+------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
+-------+-------+       +-------+-------+       +-------+-------+
|DuplicateStudent|       |StudentNotFound|       | InvalidInput  |
|     Error     |       |     Error     |       |     Error     |
+---------------+       +---------------+       +---------------+
```
*Fig. 2. Inheritance tree of system exceptions.*

*   `StudentManagementError`: Parent exception class.
*   `DuplicateStudentError`: Raised when the primary key constraint on `registration_number` is violated during creation.
*   `StudentNotFoundError`: Raised when search, update, or deletion queries target a non-existent registration number.
*   `InvalidInputError`: Raised when user entry violates validation pattern matches.

### B. Transaction Safety Framework
Because writing to multiple independent files is vulnerable to middle-execution interrupts, we wrap updates in a transactional pattern. The pseudocode below demonstrates the implementation pattern:

```python
def add_student():
    # 1. Capture inputs and validate
    # 2. Load current database records
    # 3. Raise DuplicateStudentError if registration number exists
    # 4. Clone current datasets to memory backups
    backup_csv = list(csv_records)
    backup_json = dict(json_records)
    
    # 5. Apply modifications in-memory
    csv_records.append(new_csv_entry)
    json_records[reg_no] = new_json_entry
    
    try:
        # Write to disk
        save_csv_records(csv_records)
        save_json_records(json_records)
    except Exception as write_err:
        # Transaction failed - Trigger Rollback
        save_csv_records(backup_csv)
        save_json_records(backup_json)
        raise StudentManagementError("Database write error. Rolled back.")
    finally:
        # Clean resources / finalize processes
```

### C. Logging Structure
The logging module is configured to append records to `student_system.log`. This ensures audit capabilities for monitoring actions or debugging errors. The configuration is defined as:
```python
logging.basicConfig(
    filename='student_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

---

## V. Verification & Experimental Results

To verify stability and error resistance, the system was subjected to various test runs using automated stdin redirection scripts.

### A. Test Cases and Outputs

#### 1) Read and Render All Records (Read Verification)
The system was verified to properly read, align columns, and print the existing base records correctly inside a structured grid.
*Console Output:*
```
--- View All Students ---
+--------------+----------------------+---------------------------+----------------------+-----------------+---------------------------+
| Reg No.      | Name                 | Email                     | Program              | Contact         | Address                   |
+--------------+----------------------+---------------------------+----------------------+-----------------+---------------------------+
| REG001       | John Doe             | john.doe@example.com      | Computer Science     | +1-555-0101     | 123 Maple St, Springfield |
| REG002       | Jane Smith           | jane.smith@example.com    | Information Techn... | +1-555-0102     | 456 Oak Ave, Metropolis   |
| REG003       | Bob Johnson          | bob.johnson@example.com   | Software Engineering | +1-555-0103     | 789 Pine Rd, Gotham       |
+--------------+----------------------+---------------------------+----------------------+-----------------+---------------------------+
```

#### 2) Validation Controls (Invalid Email Entry)
An attempt to insert a student with an invalid email formatting pattern (`invalid-email`) was performed to evaluate validation constraints.
*Console Output:*
```
--- Add a New Student ---
Enter Registration Number: REG005
Enter Full Name: Charlie
Enter Email Address: invalid-email
Validation Error: Email address format is invalid.
```
*Result:* The input was blocked immediately, preventing database corruption. The system raised an `InvalidInputError` and returned safely to the main menu.

#### 3) Uniqueness Constraint Validation (Duplicate Registration)
Adding a record with an existing identifier (`REG001`) was tested to verify uniqueness constraints.
*Console Output:*
```
--- Add a New Student ---
Enter Registration Number: REG001
Validation Error: A student with registration number 'REG001' already exists.
```
*Result:* System raised a `DuplicateStudentError`, logged a warning message, and cancelled the write transaction.

#### 4) Search Operation Verification
Queries for existing and non-existing registration entries were tested.
*Console Output for Non-Existent Registration Number:*
```
--- Search Student Record ---
Enter Registration Number to search: REG999
Error: Student with registration number 'REG999' was not found.
```
*Result:* Successfully raised a `StudentNotFoundError` and printed a warning, logging the search failure.

#### 5) Inline Update Operations
Updating a student record (`REG004`) was tested, replacing some parameters while leaving others blank to preserve current details.
*Console Output:*
```
Full Name [Alice Brown]: 
Email Address [alice.brown@example.com]: alice.b@example.com
Home Address [789 Pine Road]: 999 Pine Road
Contact Phone [+1-555-0104]: 
Program [Data Science]: Machine Learning
Success: Student record 'REG004' updated successfully!
```
*Result:* The fields for email, program, and address were successfully updated, while the name and contact phone number were preserved as default values.

### B. Audit Trail Analysis
Inspecting `student_system.log` confirms that all actions, inputs, warning flags, and exceptions are logged chronologically. Below is an excerpt of the log file:
```
2026-06-28 21:38:12 - INFO - Successfully added student: REG004 (Alice Brown)
2026-06-28 21:38:25 - WARNING - Add student operation failed: A student with registration number 'REG001' already exists.
2026-06-28 21:38:38 - WARNING - Add student operation failed: Email address format is invalid.
2026-06-28 21:38:48 - INFO - Student record searched and found: REG002
2026-06-28 21:38:48 - WARNING - Search failed: Student with registration number 'REG999' was not found.
2026-06-28 21:38:59 - INFO - Successfully updated student record: REG004
2026-06-28 21:39:06 - INFO - Successfully deleted student record: REG004
```

---

## VI. Conclusion

The developed **Student Record Management System** successfully fulfills the requirements of a multi-file persistent application. By separating records relationally between a CSV spreadsheet and a JSON document, the project demonstrates structural design flexibility. System resilience is secured via a strict validator layer, custom object exceptions, and a transactional rollback system. 

Future iterations could expand on this system by migrating the text files to a SQLite interface, introducing multi-user authorization levels, and adding a graphical user interface (GUI) or web interface.

---

## References

[1] IEEE Software Engineering Standards Committee, "IEEE Standard for Software Test Documentation," *IEEE Std 829-2008*, Aug. 2008.

[2] M. Pilgrim, *Dive Into Python 3*, 2nd ed. Berkeley, CA: Apress, 2009.

[3] Python Software Foundation, "CSV File Reading and Writing," *Python Documentation*, 2026. [Online]. Available: https://docs.python.org/3/library/csv.html

[4] Python Software Foundation, "JSON Encoder and Decoder," *Python Documentation*, 2026. [Online]. Available: https://docs.python.org/3/library/json.html

"""
Student Record Management System
--------------------------------
A menu-driven Python application that manages student records.
Core student details are stored in a CSV file, and additional details
are stored in a JSON file.

Features:
- Add a new student
- View all students
- Search for a student by registration number
- Update student details
- Delete a student record
- Graceful exception handling and custom exceptions
- Activity and error logging to student_system.log
"""

import csv
import json
import logging
import os
import re

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
# Resolve absolute path for files to ensure consistency
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'student_system.log')
CSV_FILE = os.path.join(BASE_DIR, 'students.csv')
JSON_FILE = os.path.join(BASE_DIR, 'students.json')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# ---------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------
class StudentManagementError(Exception):
    """Base exception class for Student Record Management System."""
    pass


class DuplicateStudentError(StudentManagementError):
    """Raised when trying to add a student with an existing registration number."""
    pass


class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student record does not exist."""
    pass


class InvalidInputError(StudentManagementError):
    """Raised when validation of input fields fails."""
    pass


# ---------------------------------------------------------
# Helper Functions for Data Storage
# ---------------------------------------------------------
def load_csv_records():
    """Reads core student records from CSV file.
    
    Returns:
        list of dict: List containing student dicts with keys: 
                      registration_number, name, email.
    """
    records = []
    if not os.path.exists(CSV_FILE):
        return records

    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Ensure the CSV header matches expected keys
            if reader.fieldnames:
                for row in reader:
                    records.append({
                        'registration_number': row.get('registration_number', '').strip(),
                        'name': row.get('name', '').strip(),
                        'email': row.get('email', '').strip()
                    })
    except Exception as e:
        logging.error(f"Failed to read CSV data: {e}")
        print(f"System Error: Failed to read CSV database file.")
    return records


def save_csv_records(records):
    """Saves core student records to CSV file.
    
    Args:
        records (list of dict): List containing student dicts to save.
    """
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['registration_number', 'name', 'email']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in records:
                writer.writerow({
                    'registration_number': rec['registration_number'].strip(),
                    'name': rec['name'].strip(),
                    'email': rec['email'].strip()
                })
    except Exception as e:
        logging.error(f"Failed to write CSV data: {e}")
        raise StudentManagementError("Failed to save changes to the CSV database.")


def load_json_records():
    """Reads additional student details from JSON file.
    
    Returns:
        dict: Dict containing extended student details keyed by registration_number.
    """
    if not os.path.exists(JSON_FILE):
        return {}

    try:
        with open(JSON_FILE, mode='r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception as e:
        logging.error(f"Failed to read JSON data: {e}")
        print(f"System Error: Failed to read JSON database file.")
        return {}


def save_json_records(records):
    """Saves additional student details to JSON file.
    
    Args:
        records (dict): Dict of extended student details to save.
    """
    try:
        with open(JSON_FILE, mode='w', encoding='utf-8') as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write JSON data: {e}")
        raise StudentManagementError("Failed to save changes to the JSON database.")


# ---------------------------------------------------------
# Input Validation Helpers
# ---------------------------------------------------------
def validate_registration_number(reg_no):
    """Validates registration number format."""
    reg_no = reg_no.strip()
    if not reg_no:
        raise InvalidInputError("Registration number cannot be empty.")
    if not re.match(r'^[a-zA-Z0-9\-_]+$', reg_no):
        raise InvalidInputError("Registration number must contain only letters, numbers, hyphens, and underscores.")
    return reg_no


def validate_name(name):
    """Validates name format."""
    name = name.strip()
    if not name:
        raise InvalidInputError("Name cannot be empty.")
    if not re.match(r'^[a-zA-Z\s\.\-]+$', name):
        raise InvalidInputError("Name must contain only alphabetic characters, spaces, dots, or dashes.")
    return name


def validate_email(email):
    """Validates email address format."""
    email = email.strip()
    if not email:
        raise InvalidInputError("Email address cannot be empty.")
    # Standard email regex pattern
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise InvalidInputError("Email address format is invalid.")
    return email


def validate_contact(contact):
    """Validates contact telephone number format."""
    contact = contact.strip()
    if not contact:
        raise InvalidInputError("Contact number cannot be empty.")
    # Matches optional '+', followed by digits, spaces, parentheses, or dashes
    pattern = r'^\+?[0-9\s\-()]{7,20}$'
    if not re.match(pattern, contact):
        raise InvalidInputError("Contact number must be a valid phone number (7-20 digits/symbols, e.g., +1-555-0199).")
    return contact


def validate_non_empty(value, field_name):
    """Validates that a string value is not empty."""
    val = value.strip()
    if not val:
        raise InvalidInputError(f"{field_name} cannot be empty.")
    return val


# ---------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------
def add_student():
    """Adds a new student to both CSV and JSON databases."""
    print("\n--- Add a New Student ---")
    try:
        # Prompt user and validate inputs
        reg_no = validate_registration_number(input("Enter Registration Number: "))
        
        # Check duplicates
        csv_records = load_csv_records()
        json_records = load_json_records()
        
        if any(rec['registration_number'].upper() == reg_no.upper() for rec in csv_records) or reg_no in json_records:
            raise DuplicateStudentError(f"A student with registration number '{reg_no}' already exists.")

        name = validate_name(input("Enter Full Name: "))
        email = validate_email(input("Enter Email Address: "))
        address = validate_non_empty(input("Enter Home Address: "), "Address")
        contact = validate_contact(input("Enter Contact Phone Number: "))
        program = validate_non_empty(input("Enter Academic Program (e.g., Computer Science): "), "Program")

        # Keep original backups in case database save fails (Atomic transactions)
        backup_csv = list(csv_records)
        backup_json = dict(json_records)

        # Update in-memory lists
        csv_records.append({
            'registration_number': reg_no,
            'name': name,
            'email': email
        })
        json_records[reg_no] = {
            'address': address,
            'contact': contact,
            'program': program
        }

        # Write updates to disks
        try:
            save_csv_records(csv_records)
            save_json_records(json_records)
            logging.info(f"Successfully added student: {reg_no} ({name})")
            print(f"\nSuccess: Student '{name}' ({reg_no}) was added successfully!")
        except Exception as write_err:
            # Rollback to ensure integrity
            save_csv_records(backup_csv)
            save_json_records(backup_json)
            logging.error(f"Transaction failed, changes rolled back. Reason: {write_err}")
            raise StudentManagementError(f"Failed to write to database: {write_err}")

    except (InvalidInputError, DuplicateStudentError) as err:
        logging.warning(f"Add student operation failed: {err}")
        print(f"\nValidation Error: {err}")
    except Exception as err:
        logging.error(f"Unexpected error in add_student: {err}", exc_info=True)
        print(f"\nError: An unexpected error occurred: {err}")
    finally:
        print("-------------------------")


def view_all_students():
    """Displays all student records combined from CSV and JSON databases."""
    print("\n--- View All Students ---")
    try:
        csv_records = load_csv_records()
        json_records = load_json_records()

        if not csv_records:
            print("No student records found in the database.")
            logging.info("View all students: database is empty.")
            return

        # Print table header
        col_widths = {
            'reg': 12,
            'name': 20,
            'email': 25,
            'program': 20,
            'contact': 15,
            'address': 25
        }
        
        border = f"+{'-'*(col_widths['reg']+2)}+{'-'*(col_widths['name']+2)}+{'-'*(col_widths['email']+2)}+{'-'*(col_widths['program']+2)}+{'-'*(col_widths['contact']+2)}+{'-'*(col_widths['address']+2)}+"
        header = f"| {'Reg No.':<{col_widths['reg']}} | {'Name':<{col_widths['name']}} | {'Email':<{col_widths['email']}} | {'Program':<{col_widths['program']}} | {'Contact':<{col_widths['contact']}} | {'Address':<{col_widths['address']}} |"
        
        print(border)
        print(header)
        print(border)

        for rec in csv_records:
            reg = rec['registration_number']
            details = json_records.get(reg, {})
            
            name = rec['name']
            email = rec['email']
            program = details.get('program', 'N/A')
            contact = details.get('contact', 'N/A')
            address = details.get('address', 'N/A')

            # Truncate strings to prevent UI layout breakage
            def trunc(s, max_w):
                return s[:max_w-3] + '...' if len(s) > max_w else s

            print(f"| {trunc(reg, col_widths['reg']):<{col_widths['reg']}} | "
                  f"{trunc(name, col_widths['name']):<{col_widths['name']}} | "
                  f"{trunc(email, col_widths['email']):<{col_widths['email']}} | "
                  f"{trunc(program, col_widths['program']):<{col_widths['program']}} | "
                  f"{trunc(contact, col_widths['contact']):<{col_widths['contact']}} | "
                  f"{trunc(address, col_widths['address']):<{col_widths['address']}} |")
        
        print(border)
        logging.info(f"Displayed all students records. Count: {len(csv_records)}")

    except Exception as err:
        logging.error(f"Error viewing all students: {err}", exc_info=True)
        print(f"Error: Could not retrieve student records: {err}")
    finally:
        print("-------------------------")


def search_student():
    """Searches for a student by their registration number."""
    print("\n--- Search Student Record ---")
    try:
        reg_no = input("Enter Registration Number to search: ").strip()
        if not reg_no:
            raise InvalidInputError("Search registration number cannot be empty.")

        csv_records = load_csv_records()
        json_records = load_json_records()

        # Find in CSV records
        student_csv = None
        for rec in csv_records:
            if rec['registration_number'].upper() == reg_no.upper():
                student_csv = rec
                # Match registration key casing in JSON database
                reg_no = rec['registration_number']
                break

        if not student_csv:
            raise StudentNotFoundError(f"Student with registration number '{reg_no}' was not found.")

        student_json = json_records.get(reg_no, {})

        print(f"\nStudent Record Found:")
        print(f"  Registration Number : {student_csv['registration_number']}")
        print(f"  Full Name           : {student_csv['name']}")
        print(f"  Email Address       : {student_csv['email']}")
        print(f"  Academic Program    : {student_json.get('program', 'N/A')}")
        print(f"  Contact Phone       : {student_json.get('contact', 'N/A')}")
        print(f"  Home Address        : {student_json.get('address', 'N/A')}")

        logging.info(f"Student record searched and found: {reg_no}")

    except (InvalidInputError, StudentNotFoundError) as err:
        logging.warning(f"Search failed: {err}")
        print(f"\nError: {err}")
    except Exception as err:
        logging.error(f"Unexpected error in search: {err}", exc_info=True)
        print(f"\nError: {err}")
    finally:
        print("-------------------------")


def update_student():
    """Updates fields of an existing student record."""
    print("\n--- Update Student Record ---")
    try:
        reg_no = input("Enter Registration Number to update: ").strip()
        if not reg_no:
            raise InvalidInputError("Registration number cannot be empty.")

        csv_records = load_csv_records()
        json_records = load_json_records()

        # Locate the record index in CSV
        idx = -1
        for i, rec in enumerate(csv_records):
            if rec['registration_number'].upper() == reg_no.upper():
                idx = i
                # Align exact key case
                reg_no = rec['registration_number']
                break

        if idx == -1 or reg_no not in json_records:
            raise StudentNotFoundError(f"Student with registration number '{reg_no}' was not found.")

        curr_csv = csv_records[idx]
        curr_json = json_records[reg_no]

        print("\nEnter new values (press Enter to keep the current value):")
        
        # Prompt and validate Name
        name_input = input(f"Full Name [{curr_csv['name']}]: ").strip()
        new_name = validate_name(name_input) if name_input else curr_csv['name']

        # Prompt and validate Email
        email_input = input(f"Email Address [{curr_csv['email']}]: ").strip()
        new_email = validate_email(email_input) if email_input else curr_csv['email']

        # Prompt and validate Address
        address_input = input(f"Home Address [{curr_json['address']}]: ").strip()
        new_address = validate_non_empty(address_input, "Address") if address_input else curr_json['address']

        # Prompt and validate Contact
        contact_input = input(f"Contact Phone [{curr_json['contact']}]: ").strip()
        new_contact = validate_contact(contact_input) if contact_input else curr_json['contact']

        # Prompt and validate Program
        program_input = input(f"Program [{curr_json['program']}]: ").strip()
        new_program = validate_non_empty(program_input, "Program") if program_input else curr_json['program']

        # Transaction backups
        backup_csv = list(csv_records)
        backup_json = dict(json_records)

        # Make modifications
        csv_records[idx] = {
            'registration_number': reg_no,
            'name': new_name,
            'email': new_email
        }
        json_records[reg_no] = {
            'address': new_address,
            'contact': new_contact,
            'program': new_program
        }

        try:
            save_csv_records(csv_records)
            save_json_records(json_records)
            logging.info(f"Successfully updated student record: {reg_no}")
            print(f"\nSuccess: Student record '{reg_no}' updated successfully!")
        except Exception as write_err:
            # Database transaction fallback
            save_csv_records(backup_csv)
            save_json_records(backup_json)
            logging.error(f"Update transaction failed, rolled back. Reason: {write_err}")
            raise StudentManagementError(f"Database write failure: {write_err}")

    except (InvalidInputError, StudentNotFoundError) as err:
        logging.warning(f"Update operation failed: {err}")
        print(f"\nError: {err}")
    except Exception as err:
        logging.error(f"Unexpected error in update: {err}", exc_info=True)
        print(f"\nError: {err}")
    finally:
        print("-------------------------")


def delete_student():
    """Deletes a student record from both CSV and JSON databases."""
    print("\n--- Delete Student Record ---")
    try:
        reg_no = input("Enter Registration Number to delete: ").strip()
        if not reg_no:
            raise InvalidInputError("Registration number cannot be empty.")

        csv_records = load_csv_records()
        json_records = load_json_records()

        # Check if record exists
        record_to_delete = None
        for rec in csv_records:
            if rec['registration_number'].upper() == reg_no.upper():
                record_to_delete = rec
                reg_no = rec['registration_number']  # Get actual case
                break

        if not record_to_delete or reg_no not in json_records:
            raise StudentNotFoundError(f"Student with registration number '{reg_no}' was not found.")

        # Show record details and confirm deletion
        print(f"\nRecord found: {record_to_delete['name']} ({reg_no})")
        confirm = input("Are you absolutely sure you want to delete this record? (yes/no): ").strip().lower()
        if confirm not in ('y', 'yes'):
            print("\nDeletion cancelled.")
            logging.info(f"Deletion of record '{reg_no}' was cancelled by user.")
            return

        # Transaction backups
        backup_csv = list(csv_records)
        backup_json = dict(json_records)

        # Modify datasets
        csv_records.remove(record_to_delete)
        del json_records[reg_no]

        try:
            save_csv_records(csv_records)
            save_json_records(json_records)
            logging.info(f"Successfully deleted student record: {reg_no}")
            print(f"\nSuccess: Student record '{reg_no}' was deleted successfully!")
        except Exception as write_err:
            # Fallback rollback
            save_csv_records(backup_csv)
            save_json_records(backup_json)
            logging.error(f"Delete transaction failed, rolled back. Reason: {write_err}")
            raise StudentManagementError(f"Database write failure during deletion: {write_err}")

    except (InvalidInputError, StudentNotFoundError) as err:
        logging.warning(f"Delete operation failed: {err}")
        print(f"\nError: {err}")
    except Exception as err:
        logging.error(f"Unexpected error in deletion: {err}", exc_info=True)
        print(f"\nError: {err}")
    finally:
        print("-------------------------")


# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------
def display_main_menu():
    """Outputs the primary system choices."""
    print("\n" + "=" * 50)
    print("        STUDENT RECORD MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add a New Student")
    print("2. View All Students")
    print("3. Search Student by Registration Number")
    print("4. Update Student Details")
    print("5. Delete Student Record")
    print("6. Exit")
    print("=" * 50)


def main():
    """Main execution loop for the command line application."""
    logging.info("Student Record Management System started.")
    
    # Verify that files are present or initialize them
    if not os.path.exists(CSV_FILE):
        try:
            save_csv_records([])
            logging.info("Created empty students.csv database file.")
        except Exception as e:
            print(f"Setup Warning: Could not create CSV database: {e}")

    if not os.path.exists(JSON_FILE):
        try:
            save_json_records({})
            logging.info("Created empty students.json database file.")
        except Exception as e:
            print(f"Setup Warning: Could not create JSON database: {e}")

    while True:
        try:
            display_main_menu()
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                logging.info("User selected Choice 1: Add Student.")
                add_student()
            elif choice == '2':
                logging.info("User selected Choice 2: View All Students.")
                view_all_students()
            elif choice == '3':
                logging.info("User selected Choice 3: Search Student.")
                search_student()
            elif choice == '4':
                logging.info("User selected Choice 4: Update Student.")
                update_student()
            elif choice == '5':
                logging.info("User selected Choice 5: Delete Student.")
                delete_student()
            elif choice == choice == '6':
                logging.info("User exited the system.")
                print("\nThank you for using the Student Record Management System. Goodbye!")
                break
            else:
                logging.warning(f"User entered invalid menu choice: '{choice}'")
                print("\nInvalid selection! Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            logging.info("System terminated via keyboard interrupt (Ctrl+C).")
            print("\n\nProgram execution interrupted. Goodbye!")
            break
        except Exception as global_err:
            logging.critical(f"Unhandled system error: {global_err}", exc_info=True)
            print(f"\nSystem Critical Error: {global_err}")
            print("Please check student_system.log for details.")
        finally:
            # Demonstrating a 'finally' block that runs after each option cycle
            pass


if __name__ == '__main__':
    main()

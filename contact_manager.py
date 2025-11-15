'''
    Name: {--Ashish Raj--}
    Date: {--15-11-2025--}
    Assignment Title: {Python-Based File Handling System For Maintaining A Contact Book}
'''

import csv
import json
import datetime
import os

# --- Global Variables ---
CONTACTS = []
CONTACT_FILE = 'contacts.csv'
JSON_FILE = 'contacts.json' 
LOG_FILE = 'error_log.txt'

# --- Utility Function for Task 6 (Error Logging) ---
def log_error(error_name, operation):
    """
        Errors ko error_log.txt file mein record karega.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ERROR: {error_name} | Operation: {operation}\n"

    try:
        # 'a' mode (append) se file mein new content judta hai
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except IOError:
        print(f"FATAL ERROR: Could not write to log file {LOG_FILE}")


# --- Task 3: Load Contacts (Reading CSV) ---
def load_contacts_from_csv():
    """Reads contacts from CSV file and loads them into the global CONTACTS list."""
    global CONTACTS
    CONTACTS.clear() # clear existing contacts before loading

    try:
        # File Handling for missing/corrupted files
        with open(CONTACT_FILE, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Each row is a dictionary with keys as column headers
                CONTACTS.append(row)

        print(f"☑️ Found {len(CONTACTS)} contacts loaded from {CONTACT_FILE}.")

    except FileNotFoundError:
        # File missing scenario: if contacts.csv file not found
        print(f"⚠️ Warning: Contact file ({CONTACT_FILE}) not found. Starting with an empty contact book.")
        log_error("FileNotFoundError", "Load contacts from CSV")

    except csv.Error as e:
        # Corrupted file scenario: if CSV file is corrupted
        print(f"❌ Error: Corrupted file ({CONTACT_FILE}). Data load failed. Error: {e}")
        log_error("CSVError", "Load contacts from CSV (Corrupted file)")
        CONTACTS.clear() # Corrupted data discard

    except Exception as e:
        error_name = type(e).__name__
        print(f"❌ An unexpected error occurred during loading: {e}")
        log_error(error_name, "Load contacts from CSV")


# --- Task 2: Save Contacts (Writing CSV) ---
def save_contacts_to_csv():
    """Helper function to save the current state of CONTACTS list to the CSV file."""
    if not CONTACTS:
        if os.path.exists(CONTACT_FILE):
             os.remove(CONTACT_FILE)
        print("ℹ️ Contact list is empty. CSV file cleared (if existed).")
        return

    try:
        # 'w' mode (write) overwrites the existing file
        with open(CONTACT_FILE, 'w', newline='') as csvfile:
            fieldnames = ['name', 'phone', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Always write the header first
            writer.writeheader()
            writer.writerows(CONTACTS)

        print(f"✅ Success: All {len(CONTACTS)} contacts saved to {CONTACT_FILE}.")

    except IOError as e:
        error_name = type(e).__name__
        print(f"❌ Error saving contacts to file: {e}")
        log_error(error_name, "Save all contacts to CSV") # Task 6 integration

    except Exception as e:
        error_name = type(e).__name__
        print(f"❌ An unexpected error occurred while saving: {e}")
        log_error(error_name, "Save all contacts to CSV") # Task 6 integration


def create_contact():
    """ Accepts contact details and saves them to contacts.csv."""

    print("\n--- New Contact Entry ---")

    # 1. Input Details
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()

    # Basic check for empty name
    if not name:
        print("❌ Error: Name cannot be empty. Contact creation aborted.")
        return

    # Check for duplicate entry before saving
    if any(c['name'].lower() == name.lower() for c in CONTACTS):
        print(f"⚠️ Warning: Contact named '{name}' already exists. Not saving duplicate.")
        return

    # 2. Store contact as dictionary and add to in-memory list
    new_contact = {'name': name, 'phone': phone, 'email': email}
    CONTACTS.append(new_contact)

    # 3. Save all contacts to CSV
    save_contacts_to_csv()


# --- Task 3: Display Contacts ---
def display_contacts():
    """Displays all contacts in a formatted, tabular way (Task 3)."""

    print("\n=======================================================")
    print("                Saved Contacts List                    ")
    print("=======================================================")

    # Handling Empty Contact Lists (Task 3 requirement)
    if not CONTACTS:
        print("ℹ️ Contacts list is empty. Add new contacts or check the CSV file.")
        return

    # Tabular Formatting Header
    print("ID\tName\t\t\tPhone Number\t\tEmail Address")
    print("------------------------------------------------------------------------")

    # Tabular format using f-strings and alignment (Task 3 requirement)
    for index, contact in enumerate(CONTACTS):
        print(f"{index+1:<4}{contact['name']:<20}\t{contact['phone']:<15}\t{contact['email']}")

    print("------------------------------------------------------------------------")


# ---------------------------------------------------------------------
# --- Task 4: Search, Update, Delete Implementation (by Name) ---
# ---------------------------------------------------------------------

# --- Helper Function for finding contacts ---
def find_contact(query):
    """
    Given a query (Name, Phone, or Email), finds matching contacts.
    """
    if not CONTACTS:
        return []

    query = query.lower().strip()
    found_matches = []

    # Check name, phone, and email for the query (case-insensitive)
    for index, contact in enumerate(CONTACTS):
        if query in contact['name'].lower() or \
           query in contact['phone'].lower() or \
           query in contact['email'].lower():
            # Index user-friendly ID ke liye
            found_matches.append((index, contact)) 

    return found_matches

# --- Helper function to find a contact's index by exact name match ---
def get_contact_index_by_name(name):
    """
    Finds the list index of a contact based on exact name match (case-insensitive).
    """
    name = name.lower().strip()
    for index, contact in enumerate(CONTACTS):
        if contact['name'].lower() == name:
            return index
    return -1


# --- Search Contact ---
def search_contact():
    """Asks user for a name/phone/email and displays matching contacts."""
    if not CONTACTS:
        print("ℹ️ Contact list is empty. Nothing to search.")
        return

    query = input("\nEnter Name, Phone, or Email to SEARCH: ").strip()
    if not query:
        print("❌ Search query cannot be empty.")
        return

    matches = find_contact(query)

    if not matches:
        print(f"\n❌ No contact found matching '{query}'.")
        return

    print("\n=======================================================")
    print(f"    Search Results for '{query}' ({len(matches)} found)")
    print("=======================================================")
    print("ID\tName\t\t\tPhone Number\t\tEmail Address")
    print("------------------------------------------------------------------------")

    for original_index, contact in matches:
        # original_index + 1 user-facing ID hai
        print(f"{original_index+1:<4}{contact['name']:<20}\t{contact['phone']:<15}\t{contact['email']}")

    print("------------------------------------------------------------------------")


# --- Update Contact (by Name) ---
def update_contact():
    """Allows user to update the details of an existing contact by Name."""
    
    if not CONTACTS:
        print("ℹ️ Contact list is empty. Cannot update.")
        return

    target_name = input("\nEnter the Name of the contact to UPDATE (Leave blank to cancel): ").strip()

    if not target_name:
        print("Update cancelled.")
        return

    contact_index = get_contact_index_by_name(target_name)

    if contact_index != -1:
        contact = CONTACTS[contact_index]
        print(f"\n--- Updating Contact: {contact['name']} ---")

        # Take new value from user, if it is blank keep old value
        new_name = input(f"Enter new Name (Current: {contact['name']}): ").strip()
        new_phone = input(f"Enter new Phone (Current: {contact['phone']}): ").strip()
        new_email = input(f"Enter new Email (Current: {contact['email']}): ").strip()

        # Name Update Validation: Check if new name is provided and is a duplicate
        final_name = contact['name']
        if new_name:
             if new_name.lower() != contact['name'].lower() and any(c['name'].lower() == new_name.lower() for c in CONTACTS):
                print(f"❌ Error: New name '{new_name}' already exists. Update aborted.")
                return
             final_name = new_name
        
        # Update the in-memory list
        CONTACTS[contact_index] = {
            'name': final_name,
            'phone': new_phone or contact['phone'], # if new value is blank use old value
            'email': new_email or contact['email']
        }
        
        # Save changes to CSV file
        save_contacts_to_csv()
        print(f"✅ Success: Contact ({final_name}) updated.")
        
    else:
        print(f"❌ Error: Contact named '{target_name}' not found.")


# --- Delete Contact (by Name) ---
def delete_contact():
    """Allows user to delete an existing contact by Name (as per assignment)."""
    
    if not CONTACTS:
        print("ℹ️ Contact list is empty. Cannot delete.")
        return

    target_name = input("\nEnter the Name of the contact to DELETE (Leave blank to cancel): ").strip()

    if not target_name:
        print("Delete cancelled.")
        return

    contact_index = get_contact_index_by_name(target_name)

    if contact_index != -1:
        deleted_contact_name = CONTACTS[contact_index]['name']
        
        # Delete from in-memory list
        del CONTACTS[contact_index] 
        
        # Save changes to CSV file
        save_contacts_to_csv()
        print(f"✅ Success: Contact ({deleted_contact_name}) deleted.")
        
    else:
        print(f"❌ Error: Contact named '{target_name}' not found.")


# --- Task 4 Controller ---
def manage_contacts():
    """Handles the Search, Update, and Delete submenu."""

    while True:
        print("\n--- S.U.D. Submenu ---")
        print("1. Search Contact (by Name/Phone/Email)")
        print("2. Update Contact (by Name)")
        print("3. Delete Contact (by Name)")
        print("4. Back to Main Menu")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            search_contact()
        elif choice == '2':
            update_contact()
        elif choice == '3':
            delete_contact()
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 4.")


# ---------------------------------------------------------------------
# --- Task 5: JSON Export/Import Implementation ---
# ---------------------------------------------------------------------

def export_to_json():
    """Task 5: Exports all contacts from the in-memory list to a JSON file."""
    if not CONTACTS:
        print("ℹ️ Contact list is empty. Nothing to export to JSON.")
        return
        
    try:
        # Open JSON file in 'w' mode
        with open(JSON_FILE, 'w') as jsonfile:
            # json.dump() Write Python objects in JSON file
            json.dump(CONTACTS, jsonfile, indent=4)
        
        print(f"✅ Success: Exported {len(CONTACTS)} contacts to {JSON_FILE}.")
        
    except IOError as e:
        error_name = type(e).__name__
        print(f"❌ Error exporting contacts to JSON file: {e}")
        log_error(error_name, "Export to JSON")


def import_from_json():
    """Task 5: Loads contacts from a JSON file, clearing the current list."""
    global CONTACTS
    
    confirm = input(f"⚠️ Warning: Loading from JSON will CLEAR {len(CONTACTS)} current contacts. Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Import cancelled.")
        return

    try:
        # Open JSON file in 'r' mode
        with open(JSON_FILE, 'r') as jsonfile:
            # json.load() Read JSON file content to list/dict in Python
            imported_contacts = json.load(jsonfile)
            
            # Validation: Ensure the imported data is a list
            if not isinstance(imported_contacts, list):
                 raise TypeError("JSON file contains invalid data structure (not a list).")
                 
            # Update global CONTACTS with new Data
            CONTACTS = imported_contacts
            
        print(f"✅ Success: Imported {len(CONTACTS)} contacts from {JSON_FILE}.")
        # Update CSV after Data load
        save_contacts_to_csv()
        display_contacts()
        
    except FileNotFoundError:
        print(f"❌ Error: JSON file ({JSON_FILE}) not found. Import failed.")
        log_error("FileNotFoundError", "Import from JSON")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Corrupted JSON file ({JSON_FILE}). Import failed. Error: {e}")
        log_error("JSONDecodeError", "Import from JSON (Corrupted file)")

    except TypeError as e:
        print(f"❌ Error: Invalid data format in JSON file. {e}")
        log_error("TypeError", "Import from JSON (Invalid data)")

    except Exception as e:
        error_name = type(e).__name__
        print(f"❌ An unexpected error occurred during import: {e}")
        log_error(error_name, "Import from JSON")


def manage_json():
    """Handles the JSON Export/Import submenu."""
    while True:
        print("\n--- JSON Submenu ---")
        print("1. Export Contacts to JSON (contacts.json)")
        print("2. Import Contacts from JSON (Overwrites current list)")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            export_to_json()
        elif choice == '2':
            import_from_json()
        elif choice == '3':
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 3.")

# ---------------------------------------------------------------------
# --- Main Application Logic ---
# ---------------------------------------------------------------------

# --- Task 1: Setup & Initialization ---
def initialize_app():
    """Sets up the project and prints the welcome message."""

    print("\n=======================================================")
    print("      Welcome to Python Contact Manager (CSV & JSON)   ")
    print("This system allows you to manage contacts using file I/O.")
    print("=======================================================")

    # Task 3: First load the contacts
    load_contacts_from_csv()


# --- Main Application Loop (Updated to call Task 5) ---
def main_menu():
    """Main loop for the application."""

    while True:
        print("\n\n--- MAIN MENU ---")
        print("1. Add New Contact") # Task 2
        print("2. View All Contacts") # Task 3
        print("3. Search/Update/Delete") # Task 4
        print("4. JSON Export/Import") # Task 5
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            create_contact()
        elif choice == '2':
            display_contacts()
        elif choice == '3':
            manage_contacts() # Task 4
        elif choice == '4':
            manage_json() # Task 5
        elif choice == '5':
            print("Exiting Contact Manager. Goodbye!")
            save_contacts_to_csv()
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 5.")


if __name__ == '__main__':
    initialize_app()
    main_menu()
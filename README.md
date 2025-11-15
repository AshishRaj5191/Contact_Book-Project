# Project Summary: Python Command-Line Contact Manager
1. Brief Project Introduction

This is a Python-based command-line application designed to efficiently manage contacts. The system utilizes File I/O (Input/Output) and Exception Handling to ensure data is stored securely and persistently.

Technologies Used: The application handles data using both the CSV (Comma Separated Values) and JSON (JavaScript Object Notation) file formats.

2. Key Features and Functionality

The application provides a complete CRUD (Create, Read, Update, Delete) system for contact management, along with robust data handling features:

A. Contact Management Operations

CRUD Operations: Users can add new contacts, view all contacts in a tabular format, search by Name/Phone/Email, and Update or Delete an existing contact using their Name as the unique identifier.

Primary Storage: All primary contact data is stored in the contacts.csv file, which is updated in real-time upon any change.

B. Data Backup and Import

JSON Export: Contacts can be exported to a contacts.json file for backup purposes.

JSON Import: Users can Import data from the JSON file, which completely overwrites the current contact list in memory.

C. Error and Security Handling

File Security: The application uses try-except blocks to handle critical I/O exceptions such as a missing file (FileNotFoundError) or corrupted file (CSVError, JSONDecodeError).

D. Error Logging (Bonus)

Exception Recording: All file-related exceptions and the operation that caused them are recorded with a timestamp in the error_log.txt file, aiding in debugging and tracking system stability.

3. Python Libraries Used

csv: Used for reading and writing the primary data storage file (contacts.csv).

json: Used for handling the backup data (Export/Import to contacts.json).

datetime: Used to generate timestamps for the error logging feature.

os: Used for checking file existence and deleting empty files.
# Student Management System

This project is a **Student Management System** built using Python and the PyQt6 framework. The application provides a GUI for managing student records, including adding, editing, searching, and deleting student data stored in a MySQL and SQLite database.

## Features

- **Add New Student:** Allows the user to insert new student records into the database.
- **Search Student:** Enables searching for a student by name.
- **Edit Student:** Provides an interface to update existing student details.
- **Delete Student:** Allows the removal of student records from the database.
- **About:** A dialog that provides information about the application.

## Prerequisites

- Python 3.x
- PyQt6
- MySQL Database
- SQLite Database

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/student-management-system.git
   cd student-management-system

2. Install the required Python packages:

   ```bash
   pip install PyQt6 mysql-connector-python

3. Ensure you have a MySQL server running and a database named school with a table students defined as follows:

   ```bash
   CREATE DATABASE school;
   
   USE school;
   
   CREATE TABLE students (
       ID INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       course VARCHAR(100),
       mobile VARCHAR(15)
   );

4. Set up the MySQL connection environment variable:

   ```bash
   export SQL_psw='your_mysql_password'
 

## File Structure
- main.py: Main script that contains the entire application logic.
- icons/: Directory containing icon images used in the application.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Feel free to modify the `README.md` to fit any additional details or preferences you might have!



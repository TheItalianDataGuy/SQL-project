from PyQt6.QtWidgets import QApplication, QLabel, \
    QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, \
    QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from PyQt6.QtCore import Qt


class DatabaseConnection:
    """This class create the connection with the database using SQLite"""
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    """This class and QMainWindow allows us to have a menu bar, a tool and status bar."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 800)

        # Set the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add subitem in File
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert_new_data)  # The Window will pop up
        file_menu_item.addAction(add_student_action)

        # Add subitem in About
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # Add subitem in Search
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search_student)  # The Window will pop up

        about_action.setMenuRole(QAction.MenuRole.NoRole)  # In case the bar is not shown (Mac)

        # Set the table with columns and headers' labels
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # to hide the default index column
        self.setCentralWidget(self.table)

        # Instantiate the toolbar class
        toolbar = QToolBar()
        # The toolbar can be moved by the user
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        # Add elements to the toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar and its elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click so that the Edit/Delete buttons appear
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        """This method  will load the data from the database"""
        # Create a connection with the database
        connection = sqlite3.connect("database.db")
        extract = connection.execute("SELECT * FROM students")

        # It makes sure that the new data is not overwritten on top of the old data
        self.table.setRowCount(0)

        # for loop to load the data from the database
        # 1st loop: put the data in rows
        # 2nd loop: insert the data in columns
        for row_number, row_data in enumerate(extract):
            self.table.insertRow(row_number)
            print(row_data)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                print(data)
        connection.close()

    # This class will let the edit button appear when a cell is clicked
    def cell_clicked(self):
        """This method let the edit button appear when a cell is clicked"""
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # To avoid to duplicate the same buttons every time a cell is clicked
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add the widgets after the children if statement
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    # This class will save the new data from the add student window
    def insert_new_data(self):
        """This class creates the add dialog box"""
        dialog = InsertDialog()
        dialog.exec()

    def search_student(self):
        """This class creates the search dialog box"""
        dialog = SearchStudent()
        dialog.exec()

    def edit(self):
        """This class creates the edit dialog box"""
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        """This class creates the delete dialog box"""
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        """This class creates the 'about' dialog box"""
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    """This class creates the add student window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        # Add cancel button
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.close_window)
        layout.addWidget(cancel)

        self.setLayout(layout)

    def add_student(self):
        """This method creates the connection to the database and add the new student"""
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.accept()  # It closes the Add Student Window

    def close_window(self):
        """This method closes the Add Student Window if cancel button pressed."""
        self.accept()  # It closes the Add Student Window if cancel button pressed.


# Search window
class SearchStudent(QDialog):
    """This class creates the search window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add name box
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add search button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        """This method searches for the name of the student inserted and highlights the name in the table"""

        # Select the name typed in the box
        name = self.student_name.text()
        # Create a connection with the database
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        # Find the name in the database
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        # Convert the object into a list
        names_in_database = list(result)
        print(names_in_database)
        # We access the table object of the class main_window. However, they are still objects
        names_from_table = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        # Select the names in the table
        for name in names_from_table:
            print(name)
            main_window.table.item(name.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        self.accept()


class EditDialog(QDialog):
    """This class creates the edit student window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # To identify the student selected from table
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # To get the ID of a selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Show student name widget
        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        # Add combo box of courses
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile_number = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile_number)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add update button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        # Add cancel button
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.close_window)
        layout.addWidget(cancel)

        self.setLayout(layout)

    def close_window(self):
        self.accept()  # It closes the Add Student Window if cancel button pressed.

    def update_student(self):
        """This method updates the student contact details"""
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?,"
                       " mobile = ? WHERE ID = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit() # UPDATE is a write operations so commit() is needed
        cursor.close()
        connection.close()

        # Refresh the table
        main_window.load_data()
        self.accept()


class DeleteDialog(QDialog):
    """This class creates the delete student window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()

        # Create Widget for delete student
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        # Add widget to the layout
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        # Create a delete action when clicked yes/no
        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        """This method can delete the student selected"""

        # To identify the student selected from table
        index = main_window.table.currentRow()

        # To get the ID of a selected row
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE ID = ?", (student_id, ))
        # needs a comma in the parameters otherwise the tuple is not recognised
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data() # Refresh the table
        self.accept()

        # Create a confirmation message of deletion
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


class AboutDialog(QMessageBox):
    """This class creates the 'about' window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """This app was created during a Python course.
        Feel free to modify and reuse this app."""
        self.setText(content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

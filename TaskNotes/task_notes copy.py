"""
Docstring for task_notes 10 days project
"""

from datetime import datetime
import json
import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QMessageBox,
    QWidget,
)

from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Notes")
        self.setGeometry(700, 300, 500, 500)
        self.setWindowIcon(QIcon("appIcon.png"))
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.delete_button = QPushButton("Delete current task", self)
        self.save_button = QPushButton("Save", self)
        self.load_button = QPushButton("Load", self)
        self.task_list = QComboBox(self)
        self.priority_level = QComboBox(self)
        self.description_field = QTextEdit(self)
        self.print_dic_button = QPushButton("Print tasks", self)
        self.clear_dic_button = QPushButton("Clear tasks", self)
        self.label1 = QLabel(self)
        self.date_label = QLabel("Created", self)
        self.priority_label = QLabel("Priority level:", self)
        self.stored_tasks = {
            "Example task": {
                "description": "Example description",
                "date": datetime.now().strftime("%c"),
                "priority": "Low",
            },
            "Example task2": {
                "description": "Example description2",
                "date": datetime.now().strftime("%c"),
                "priority": "Low",
            },
        }
        # self.completer = QCompleter(self.stored_tasks, self)
        # self.completer.setCaseSensitivity(Qt.CaseSensitive)
        self.init_ui()
        self.init_widgets()
        self.init_connections()

    def init_ui(self):
        """UI initialization function"""
        # ComboBox list of priority levels
        self.priority_level.setVisible(False)
        self.priority_level.addItems(["High", "Medium", "Low"])
        self.priority_level.setCurrentText("Low")
        self.label1.setStyleSheet("font-size:15px;")

        self.date_label.setStyleSheet("font-size:15px;")
        # Delete Button
        self.delete_button.setHidden(True)

        # ComboBox List Of Tasks
        self.task_list.setEditable(True)
        self.task_list.setInsertPolicy(QComboBox.InsertAtBottom)
        self.task_list.setInsertPolicy(QComboBox.NoInsert)


        # Text Field
        self.description_field.setStyleSheet("font-size:15px;")
        self.description_field.setUndoRedoEnabled(True)
        self.description_field.setPlaceholderText("No description yet!")

        self.line_edit = self.task_list.lineEdit()

        # Runs (Inits Application) If Dictionary Is Not Empty At The Start Of The Program
        if self.stored_tasks:
            self.delete_button.setVisible(True)
            self.label1.setText("Modifying is available")
            self.date_label.setText(f"Created: {self.get_date()}")
            for task in self.stored_tasks:
                self.task_list.addItem(task)
            self.display_description()
            self.priority_level.setVisible(True)

    def init_connections(self):
        """Widgets connections initialization function"""
        # Delete Confirmation Button
        self.delete_button.clicked.connect(self.show_message)
        # Load Buttons
        self.save_button.clicked.connect(self.save_task)
        self.load_button.clicked.connect(self.load_task)

        # Debug Buttons
        self.print_dic_button.clicked.connect(self.print_dic)
        self.clear_dic_button.clicked.connect(self.clear_tasks)

        # Task Logic Connections
        self.task_list.currentTextChanged.connect(self.show_ui_elements)
        if self.line_edit is not None:
            self.line_edit.editingFinished.connect(self.add_task)
            self.line_edit.editingFinished.connect(self.task_ui)
            #self.line_edit.returnPressed.connect(self.return_pressed_double_item_fix)
        self.task_list.currentTextChanged.connect(self.display_description)

        self.description_field.textChanged.connect(self.add_description)

        self.priority_level.currentTextChanged.connect(self.set_priority_level)

    def init_widgets(self):
        """Widgets initialization function"""
        # Add main widgets to the vertical layout
        self.vbox.addWidget(self.task_list)
        self.vbox.addWidget(self.description_field)

        # --- Horizontal layout for priority label + ComboBox ---
        self.hbox_priority = QHBoxLayout()
        self.hbox_priority.addWidget(self.priority_label)  # Label on the left
        self.hbox_priority.addWidget(self.priority_level)  # ComboBox on the right
        self.hbox_priority.addStretch(1)  # Optional: pushes everything left
        self.vbox.addLayout(self.hbox_priority)  # Add the priority row to main vbox

        # --- Top row of buttons / labels ---
        self.hbox_top = QHBoxLayout()
        self.hbox_top.addWidget(self.print_dic_button)
        self.hbox_top.addWidget(self.clear_dic_button)
        self.hbox_top.addWidget(self.label1)
        self.hbox_top.addWidget(self.date_label)
        self.vbox.addLayout(self.hbox_top)

        # --- Bottom row of action buttons ---
        self.hbox_bottom = QHBoxLayout()
        self.hbox_bottom.addWidget(self.save_button)
        self.hbox_bottom.addWidget(self.delete_button)
        self.hbox_bottom.addWidget(self.load_button)
        self.vbox.addLayout(self.hbox_bottom)

        central_widget = QWidget()
        central_widget.setLayout(self.vbox)
        self.setCentralWidget(central_widget)

    # Functions

    def show_ui_elements(self):
        """UI elements in different UI states"""
        task = self.task_list.currentText()
        self.description_field.setEnabled(True)
        self.label1.setVisible(True)
        self.date_label.setVisible(False)
        self.priority_level.setVisible(False)
        self.delete_button.setVisible(False)
        if not task:
            self.description_field.setEnabled(False)
            self.label1.setText("Add task before modifying description")
            self.line_edit.setFocus()
            return
        if task not in self.stored_tasks:
            self.label1.setText("Task will be added automatically")
        else:
            self.delete_button.setVisible(True)
            self.label1.setVisible(True)
            self.label1.setText("Modifying is available")
            self.date_label.setVisible(True)
            self.date_label.setText(self.stored_tasks[task]["date"])
            self.priority_level.setVisible(True)

    def add_task(self):
        """Adds task when return pressed or comboBox lineEdit focus out"""
        task = self.task_list.currentText()
        if not task:
            return
        if task not in self.stored_tasks:
            self.stored_tasks[task] = {
                "description": "",
                "date": self.get_date(),
                "priority": "Low",
            }
            self.task_list.addItem(task)
            self.task_list.setCurrentText(task)
            print("Task Added")
            self.label1.setText("Task added!")
            self.priority_level.setCurrentText("Low")

    def task_ui(self):
        """Enables UI elements when user modifies description"""
        if self.task_list.currentText():
            self.description_field.setEnabled(True)
            self.description_field.setFocus()
            self.delete_button.setVisible(True)
            cursor = self.description_field.textCursor()
            cursor.movePosition(cursor.End)
            self.description_field.setTextCursor(cursor)
            self.priority_level.setVisible(True)
            print("label1 turned off")
            self.date_label.setVisible(True)

    def set_priority_level(self):
        """
        Adds priority level to the current task
        """
        if self.task_list.currentText() in self.stored_tasks:

            self.stored_tasks[self.task_list.currentText()][
                "priority"
                ] = self.priority_level.currentText()

    def add_description(self):
        """Adds description to current task in comboBox lineEdit"""
        task = self.task_list.currentText()
        if task in self.stored_tasks:
            self.stored_tasks[task][
                "description"
            ] = self.description_field.toPlainText()
            # self.date_label.setVisible(True)
            # self.date_label.setText(self.stored_tasks[task]["date"])
            self.label1.setVisible(False)

    def display_description(self):
        """Displays Description When Task (CurrentText/CurrentIndex) In ComboBox Changes"""
        task = self.task_list.currentText()
        if task in self.stored_tasks:
            self.description_field.setText(self.stored_tasks[task]["description"])
            self.date_label.setText(self.stored_tasks[task]["date"])
            self.priority_level.setCurrentText(self.stored_tasks[task]["priority"])
        else:
            self.description_field.setText("")
        cursor = self.description_field.textCursor()
        cursor.movePosition(cursor.End)
        self.description_field.setTextCursor(cursor)
        print(1)

    def delete_task(self):
        """Deletes Current Task And Sets currentIndex - 1"""
        current_index = self.task_list.currentIndex()
        current_text = self.task_list.currentText()

        self.stored_tasks.pop(current_text, None)
        self.task_list.removeItem(current_index)
        if not self.stored_tasks:
            self.task_list.clear()
            self.stored_tasks.clear()
            self.label1.setText("Add task by typing it's name in the text field!")
            self.description_field.setEnabled(False)
            print("Deleted all tasks")
        elif current_index == 0:
            print("Deleting Index is 0")
            self.task_list.setCurrentIndex(current_index)
        elif current_index != 0:
            self.task_list.setCurrentIndex(current_index - 1)
            print("Deleting Index is not 0")
        self.line_edit.setFocus()

    def show_message(self):
        """Confirmation Message on Task Deletion"""
        reply = QMessageBox.question(
            self,
            "Delete task",
            "Are you sure you want to delete the current task",
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Ok,
        )
        if reply == QMessageBox.Ok:
            self.delete_task()

    def save_task(self):
        """Saves (Writes) Task To File tasksSaved.json"""
        with open("tasksSaved.json", "w", encoding="utf-8") as f:
            json.dump(self.stored_tasks, f)

    def load_task(self):
        """Loads Dictionary File With Tasks If The File Exists"""
        try:
            with open("tasksSaved.json", "r", encoding="utf-8") as stored_tasks_save:
                copy = json.load(stored_tasks_save)
            if self.stored_tasks != copy:
                self.stored_tasks.clear()
                self.task_list.clear()
                for task, description in copy.items():
                    self.stored_tasks[task] = description
                    self.task_list.addItem(task)
                if self.task_list.currentText() == "":
                    self.task_list.setCurrentIndex(self.task_list.currentIndex() + 1)
                self.label1.setText(
                    f"Successfully added {len(self.stored_tasks) + 1} tasks"
                )
                self.description_field.setEnabled(True)
            else:
                self.label1.setText("Loading tasks are identical to the current tasks!")
                return
        except FileNotFoundError:
            self.label1.setText(
                "File not found, you need to save it before loading it!"
            )
        except PermissionError:
            self.label1.setText("Permission denied when accessing tasksSaved.json.")
        except IOError as e:
            self.label1.setText(f"An I/O error occurred: {e}")

    def print_dic(self):
        """Debug Button: Prints Dictionary"""
        print(self.stored_tasks)

    def clear_tasks(self):
        """Debug Button: Clears Dictionary And ComboBox"""
        self.stored_tasks.clear()
        self.task_list.clear()
        self.description_field.setEnabled(False)
        self.line_edit.setFocus()
        self.label1.setText("Add task by typing it's name in the text field!")

    def get_date(self):
        """
        Gets current date
        """
        return datetime.now().strftime("%c")

    def return_pressed_double_item_fix(self):
        """Fix for comboBox editable"""
        task = self.task_list.currentText()
        self.task_list.removeItem(self.task_list.currentIndex())
        self.task_list.setCurrentText(task)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    STYLE = """
    QPushButton:hover {
    background-color: gray;}
    """
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

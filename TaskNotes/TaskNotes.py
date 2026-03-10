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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
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
        self.description_field = QTextEdit(self)
        self.print_dic_button = QPushButton("Print tasks", self)
        self.clear_dic_button = QPushButton("Clear tasks", self)
        self.label1 = QLabel(self)
        self.stored_tasks = {
            "Example task": "Example description",
            "Example task2": "Example description2",
            "Buy milk": "2 liters",
            "Call mom": "at 18:00",
            "Meeting": "tomorrow 10am",
        }
        #self.completer = QCompleter(self.stored_tasks, self)
        #self.completer.setCaseSensitivity(Qt.CaseSensitive)
        self.initUI()
        self.initWidgets()
        self.initConnections()

    def initUI(self):
        self.label1.setStyleSheet("font-size:15px;")
        # Delete Button
        self.delete_button.setHidden(True)

        # ComboBox List Of Tasks
        self.task_list.setEditable(True)
        self.task_list.setInsertPolicy(QComboBox.InsertAtBottom)

        # Text Field
        self.description_field.setStyleSheet("font-size:15px;")
        self.description_field.setUndoRedoEnabled(True)
        self.description_field.setPlaceholderText("No description yet!")

        self.lineEdit = self.task_list.lineEdit()

        # Runs (Inits Application) If Dictionary Is Not Empty At The Start Of The Program
        if self.stored_tasks:
            self.delete_button.setVisible(True)
            self.label1.setText("Modifying is available")
            for task in self.stored_tasks:
                self.task_list.addItem(task)
            self.display_description()

    def initConnections(self):
        # Delete Confirmation Button
        self.delete_button.clicked.connect(self.show_message)
        # Load Buttons
        self.save_button.clicked.connect(self.save_task)
        self.load_button.clicked.connect(self.load_task)

        # Debug Buttons
        self.print_dic_button.clicked.connect(self.print_dic)
        self.clear_dic_button.clicked.connect(self.clear_tasks)

        # Task Logic Connections
        self.task_list.currentTextChanged.connect(self.display_description)
        self.task_list.currentTextChanged.connect(self.show_UI_elements)
        if self.lineEdit is not None:
            self.lineEdit.editingFinished.connect(self.add_task)
            self.lineEdit.editingFinished.connect(self.task_UI)
            self.lineEdit.returnPressed.connect(self.return_pressed_double_item_fix)

        self.description_field.textChanged.connect(self.add_description)

    def initWidgets(self):
        # Widgets placing
        self.vbox.addWidget(self.task_list)
        self.vbox.addWidget(self.description_field)
        self.vbox.addWidget(self.print_dic_button)
        self.vbox.addWidget(self.clear_dic_button)
        self.vbox.addWidget(self.label1)

        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.delete_button)
        self.hbox.addWidget(self.load_button)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        centralWidget = QWidget()
        centralWidget.setLayout(self.vbox)
        self.setCentralWidget(centralWidget)

    # Functions

    def show_UI_elements(self):
        if not self.task_list.currentText():
            self.description_field.setEnabled(False)
            return
        if self.task_list.currentText() not in self.stored_tasks:
            self.delete_button.setVisible(False)
            self.label1.setVisible(True)
            self.label1.setText("Task will be added automatically")
            self.description_field.setEnabled(True)
        else:
            self.delete_button.setVisible(True)
            self.label1.setVisible(True)
            self.label1.setText("Modifying is available")

    def return_pressed_double_item_fix (self):
        task = self.task_list.currentText()
        self.task_list.removeItem(self.task_list.currentIndex())
        self.task_list.setCurrentText(task)

    def add_task (self):
        task = self.task_list.currentText()
        if not task:
            self.label1.setText("Add task before modifying description")
            self.description_field.setEnabled(False)
            self.lineEdit.setFocus()
            return
        if task not in self.stored_tasks:
            self.stored_tasks[task] = ""
            self.task_list.addItem(task)
            self.task_list.setCurrentText(task)
            self.label1.setText("Task added!")
            print("Task Added")

    def task_UI (self):
        self.description_field.setFocus()
        self.delete_button.setVisible(True)
        self.description_field.setEnabled(True)
        cursor = self.description_field.textCursor()
        cursor.movePosition(cursor.End)
        self.description_field.setTextCursor(cursor)


    def add_description (self):
        if self.task_list.currentText() in self.stored_tasks:
            self.stored_tasks[self.task_list.currentText()] = self.description_field.toPlainText()
            self.label1.setVisible(False)

    def display_description(self):
        # Displays Description When Task (CurrentText/CurrentIndex) In ComboBox Changes
        self.description_field.setText(self.stored_tasks.get(self.task_list.currentText()))
        cursor = self.description_field.textCursor()
        cursor.movePosition(cursor.End)
        self.description_field.setTextCursor(cursor)
        print(1)

    def show_message(self):
        # Confirmation Message on Task Deletion
        reply = QMessageBox.question(
            self,
            "Delete task",
            "Are you sure you want to delete the current task",
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Ok,
        )
        if reply == QMessageBox.Ok:
            self.delete_task()

    def delete_task(self):
        # Deletes Current Task And Sets currentIndex - 1
        currentIndex = self.task_list.currentIndex()
        currentText = self.task_list.currentText()

        self.stored_tasks.pop(currentText, None)
        self.task_list.removeItem(currentIndex)
        if not self.stored_tasks:
            self.task_list.clear()
            self.stored_tasks.clear()
            self.label1.setText("Add task by typing it's name in the text field!")
            self.description_field.setEnabled(False) 
            print("Deleted all tasks")
        elif currentIndex == 0:
            print("Deleting Index is 0")
            self.task_list.setCurrentIndex(currentIndex)
        elif currentIndex != 0:
            self.task_list.setCurrentIndex(currentIndex - 1)
            print("Deleting Index is not 0")
        self.lineEdit.setFocus()

    def save_task(self):
        # Saves (Writes) Task To File tasksSaved.json
        with open("tasksSaved.json", "w", encoding="utf-8") as f:
            json.dump(self.stored_tasks, f)

    def load_task(self):
        # Loads Dictionary File With Tasks If The File Exists
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
                self.label1.setText(f"Successfully added {len(self.stored_tasks) + 1} tasks")
                self.description_field.setEnabled(True)
            else:
                self.label1.setText("Loading tasks are identical to current tasks!")
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
        # Debug Button: Prints Dictionary
        print(self.stored_tasks)

    def clear_tasks(self):
        # Debug Button: Clears Dictionary And ComboBox
        self.stored_tasks.clear()
        self.task_list.clear()
        self.label1.setText("Add task by typing it's name in the text field!")
        self.description_field.setEnabled(False) 
        self.lineEdit.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

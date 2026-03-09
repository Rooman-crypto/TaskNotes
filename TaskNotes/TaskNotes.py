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
        self.deleteButton = QPushButton("Delete current task", self)
        self.saveButton = QPushButton("Save", self)
        self.loadButton = QPushButton("Load", self)
        self.taskList = QComboBox(self)
        self.descriptionField = QTextEdit(self)
        self.button = QPushButton("Print tasks", self)
        self.button2 = QPushButton("Clear tasks", self)
        self.label1 = QLabel(self)
        self.storedTasks = {
            "Example task": "Example description",
            "Example task2": "Example description2",
            "Buy milk": "2 liters",
            "Call mom": "at 18:00",
            "Meeting": "tomorrow 10am",
        }
        #self.completer = QCompleter(self.storedTasks, self)
        #self.completer.setCaseSensitivity(Qt.CaseSensitive)
        self.initUI()
        self.initWidgets()
        self.initConnections()

    def initUI(self):
        self.label1.setStyleSheet("font-size:15px;")
        # Delete Button
        self.deleteButton.setHidden(True)

        # ComboBox List Of Tasks
        self.taskList.setEditable(True)
        self.taskList.setInsertPolicy(QComboBox.InsertAtBottom)

        # Text Field
        self.descriptionField.setStyleSheet("font-size:15px;")
        self.descriptionField.setUndoRedoEnabled(True)
        self.descriptionField.setPlaceholderText("No description yet!")

        self.lineEdit = self.taskList.lineEdit()

        # Runs (Inits Application) If Dictionary Is Not Empty At The Start Of The Program
        if self.storedTasks:
            self.deleteButton.setVisible(True)
            self.label1.setText("Enter to modify the task!")
            for task in self.storedTasks:
                self.taskList.addItem(task)
            self.displayDescription()

    def initConnections(self):
        # Delete Confirmation Button
        self.deleteButton.clicked.connect(self.showMessage)
        # Load Buttons
        self.saveButton.clicked.connect(self.saveTask)
        self.loadButton.clicked.connect(self.loadTask)

        # Debug Buttons
        self.button.clicked.connect(self.printDic)
        self.button2.clicked.connect(self.clearTasks)

        # Task Logic Connections
        self.taskList.currentTextChanged.connect(self.displayDescription)
        self.taskList.currentTextChanged.connect(self.showUIElements)
        if self.lineEdit is not None:
            self.lineEdit.editingFinished.connect(self.addTask)
            self.lineEdit.returnPressed.connect(self.returnPressedDoubleItemFix)

        self.descriptionField.textChanged.connect(self.addDescription)

    def initWidgets(self):
        # Widgets placing
        self.vbox.addWidget(self.taskList)
        self.vbox.addWidget(self.descriptionField)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.label1)

        self.hbox.addWidget(self.saveButton)
        self.hbox.addWidget(self.deleteButton)
        self.hbox.addWidget(self.loadButton)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        centralWidget = QWidget()
        centralWidget.setLayout(self.vbox)
        self.setCentralWidget(centralWidget)

    # Functions

    def showUIElements(self):
        if self.taskList.currentText() not in self.storedTasks:
            self.deleteButton.setVisible(False)
            self.label1.setVisible(True)
            self.label1.setText("Task will be added automatically")
        else:
            self.deleteButton.setVisible(True)
            self.label1.setVisible(True)
            self.label1.setText("Enter to modify the task")

    def returnPressedDoubleItemFix (self):
        task = self.taskList.currentText()
        self.taskList.removeItem(self.taskList.currentIndex())
        self.taskList.setCurrentText(task)

    def addTask (self):
        task = self.taskList.currentText()
        if not task:
            self.label1.setText("Task field can't be empty!")
            self.descriptionField.setEnabled(False)
            return
        if task not in self.storedTasks:
            self.storedTasks[task] = ""
            self.taskList.addItem(task)
            self.taskList.setCurrentText(task)
            self.label1.setText("Task added!")
            print("Task Added")
        self.descriptionField.setFocus()
        self.deleteButton.setVisible(True)
        self.descriptionField.setEnabled(True)
        cursor = self.descriptionField.textCursor()
        cursor.movePosition(cursor.End)
        self.descriptionField.setTextCursor(cursor)

    def addDescription (self):
        if self.taskList.currentText() in self.storedTasks:
            self.storedTasks[self.taskList.currentText()] = self.descriptionField.toPlainText()
            self.label1.setVisible(False)

    def displayDescription(self):
        # Displays Description When Task (CurrentText/CurrentIndex) In ComboBox Changes
        self.descriptionField.setText(self.storedTasks.get(self.taskList.currentText()))
        cursor = self.descriptionField.textCursor()
        cursor.movePosition(cursor.End)
        self.descriptionField.setTextCursor(cursor)

    def showMessage(self):
        # Confirmation Message on Task Deletion
        reply = QMessageBox.question(
            self,
            "Delete task",
            "Are you sure you want to delete the current task",
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Ok,
        )
        if reply == QMessageBox.Ok:
            self.deleteTask()

    def deleteTask(self):
        # Deletes Current Task And Sets currentIndex - 1
        currentIndex = self.taskList.currentIndex()
        currentText = self.taskList.currentText()

        self.storedTasks.pop(currentText, None)
        self.taskList.removeItem(currentIndex)
        if not self.storedTasks:
            self.taskList.clear()
            self.storedTasks.clear()
            self.label1.setText("Add task by typing it's name in the text field!")
            print("Deleted all tasks")
        elif currentIndex == 0:
            print("Deleting Index is 0")
            self.taskList.setCurrentIndex(currentIndex)
        elif currentIndex != 0:
            self.taskList.setCurrentIndex(currentIndex - 1)
            print("Deleting Index is not 0")
        self.lineEdit.setFocus()

    def saveTask(self):
        # Saves (Writes) Task To File tasksSaved.json
        with open("tasksSaved.json", "w", encoding="utf-8") as f:
            json.dump(self.storedTasks, f)

    def loadTask(self):
        # Loads Dictionary File With Tasks If The File Exists
        try:
            with open("tasksSaved.json", "r", encoding="utf-8") as storedTasksSave:
                copy = json.load(storedTasksSave)
            if self.storedTasks != copy:
                self.storedTasks.clear()
                self.taskList.clear()
                for task, description in copy.items():
                    self.storedTasks[task] = description
                    self.taskList.addItem(task)
                if self.taskList.currentText() == "":
                    self.taskList.setCurrentIndex(self.taskList.currentIndex() + 1)
                self.label1.setText(f"Successfully added {len(self.storedTasks) + 1} tasks")
            else:
                self.label1.setText("Loading Tasks are identical to current tasks!")
                return
        except FileNotFoundError:
            self.label1.setText(
                "File not found, you need to save it before loading it!"
            )
        except PermissionError:
            self.label1.setText("Permission denied when accessing tasksSaved.json.")
        except IOError as e:
            self.label1.setText(f"An I/O error occurred: {e}")

    def printDic(self):
        # Debug Button: Prints Dictionary
        print(self.storedTasks)

    def clearTasks(self):
        # Debug Button: Clears Dictionary And ComboBox
        self.storedTasks.clear()
        self.taskList.clear()
        self.label1.setText("Add task by typing it's name in the text field!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

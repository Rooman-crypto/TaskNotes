# TaskNotes

## Description

- Application, that lets user create tasks in a notepad/ to do apps way.
- Description, that can be attached to the created task.

# Used tools

- VScode
- Nvim
- pytest (for stating testing)
- pylint

# Used Python libraries

- PyQt5
- Json

# Architecture

- Hash table aka Python dictionaries for the source of truth.
- Widgets from PyQt5 library e.g. (buttton, comboBox, textField) for the application flow.
- Json is used to store tasks for the use after restart of the application.
- In order to save tasks, user needs to press save button, and in order to load them user needs to press load button.

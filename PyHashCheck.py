# Copyright (c) Michael Stilson 2023
# This program is free software; you can redistribute it and/or
# modify it under the terms of the MIT License.

# Imports for application.
import os
import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QWidget, QFileDialog, QGridLayout, QMessageBox, QProgressBar, QComboBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

# Application version.
VERSION = "1.0.0"

# Initialize app.
app = QApplication(sys.argv)

# Initialize window.
window = QWidget()
window.setWindowTitle("PyHashCheck")
window.setWindowIcon(QtGui.QIcon('PyHashCheck.png'))

# Function to create buttons of all the same style.
def create_buttons(button_text):
    button = QPushButton(button_text)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(150)
    return button

# Function to create labels with the same style
def create_labels(label_text):
    label = QLabel(label_text)
    return label

# Function to open a native file picker to select a file to hash.
def get_file():
    filename = QFileDialog().getOpenFileName(None, 'Select File')
    return filename

# Function to extract the file path returned from Get_file() then update the path in the UI and selceted file variable.
def update_selected_file():
    global selected_file
    file = get_file()
    if file:
        print(file[0])
        selected_file_label.setText("Selected File: " + str(file[0]))
    selected_file = file[0]

# Function that actually calulates the selected files hash, and compares it to the expected value.
# This function also updates the progress bar, calculates current progress, an launches result dialog boxes.
def calculate_hash():
    file_path = selected_file
    expected_hash = input_hash_box.text()

    if (file_path == ""):
        return

    block_size = 65536

    if (alg_box.currentText() == "md5"):
        print("Selected: md5")
        file_hash = hashlib.md5()
    elif (alg_box.currentText() == "sha1"):
        print("Selected: sha1")
        file_hash = hashlib.sha1()
    elif (alg_box.currentText() == "sha224"):
        print("Selected: sha224")
        file_hash = hashlib.sha224()
    elif (alg_box.currentText() == "sha256"):
        print("Selected: sha256")
        file_hash = hashlib.sha256()
    elif (alg_box.currentText() == "sha384"):
        print("Selected: sha384")
        file_hash = hashlib.sha384()
    elif (alg_box.currentText() == "sha512"):
        print("Selected: sha512")
        file_hash = hashlib.sha512()

    total_size = os.path.getsize(file_path)

    with open(file_path, 'rb') as f:
        fb = f.read(block_size)
        progress_bar.setValue(int(f.tell()) * 100 / int(total_size))
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
            progress_bar.setValue(int(f.tell()) * 100 / int(total_size))
    
    if (file_hash.hexdigest() == expected_hash):
        print("Hashes match!")
        QMessageBox.information(None, "Hash Calculated", "Hashes match!")
    else:
        print("Hashes do not match!")
        QMessageBox.warning(None, "Hash Calculated", "Hashes do not match!")

# Function to reset the forms and selected file in the applicaiton.
def reset_forms():
    global selected_file
    selected_file = ""
    selected_file_label.setText("Selected File: " + selected_file)
    input_hash_box.setText("")
    progress_bar.setValue(0)

# Initialize selected file as null.
selected_file = ""

# Initialize various UI Widgets.
selected_file_label = create_labels("Selected File: " + str(selected_file))
selected_file_label.setWordWrap(True)

input_hash_label = create_labels("Enter expected hash: ")
input_hash_box = QLineEdit(None)

alg_label = create_labels("Select hash mode: ")
alg_box = QComboBox()
alg_box.addItems(["md5", "sha1", "sha224", "sha256", "sha384", "sha512"])

progress_bar = QProgressBar()
progress_bar.setValue(0)

calculate_button = create_buttons("Check Hash")
calculate_button.clicked.connect(calculate_hash)

select_file_button = create_buttons("Select File")
select_file_button.clicked.connect(update_selected_file)

reset_button = create_buttons("Reset")
reset_button.clicked.connect(reset_forms)

# Initialize grid and add widgets.
grid = QGridLayout()

window.setLayout(grid)

grid.addWidget(selected_file_label, 0, 0, 1, 6)
grid.addWidget(input_hash_label, 1, 0)
grid.addWidget(input_hash_box, 1, 1, 1, 2)
grid.addWidget(alg_label, 2, 0)
grid.addWidget(alg_box, 2, 1, 1, 2)
grid.addWidget(progress_bar, 3, 0, 1, 6)
grid.addWidget(reset_button, 4, 0)
grid.addWidget(select_file_button, 4, 1)
grid.addWidget(calculate_button, 4, 2)

# Display window.
window.show()

# Terminate app.
sys.exit(app.exec())
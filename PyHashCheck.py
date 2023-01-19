# Imports for application.
import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QWidget, QFileDialog, QGridLayout, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

# Initialize app.
app = QApplication(sys.argv)

# Initialize window.
window = QWidget()
window.setWindowTitle("PyHashCheck")
window.setFixedWidth(500)
#window.setStyleSheet("background: #161219;")

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

def get_file():
    filename = QFileDialog().getOpenFileName(None, 'Select File')
    return filename

def update_selected_file():
    global selected_file
    file = get_file()
    if file:
        print(file[0])
        selected_file_label.setText("Selected File: " + str(file[0]))
    selected_file = file[0]

def calculate_hash():
    file_path = selected_file
    expected_hash = input_hash_box.text()
    algorithm = "sha256"

    if (file_path == ""):
        return

    block_size = 65536

    if (algorithm == "sha256"):
        file_hash = hashlib.sha256()
    else:
        file_hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
    
    if (file_hash.hexdigest() == expected_hash):
        print("Hashes match!")
        QMessageBox.information(None, "Hash Calculated", "Hashes match!")
    else:
        print("Hashes do not match!")
        QMessageBox.warning(None, "Hash Calculated", "Hashes do not match!")

def reset_forms():
    global selected_file
    selected_file = ""
    selected_file_label.setText("Selected File: " + selected_file)
    input_hash_box.setText("")

selected_file = ""

selected_file_label = create_labels("Selected File: " + str(selected_file))
selected_file_label.setWordWrap(True)

input_hash_label = create_labels("Enter expected hash: ")
input_hash_box = QLineEdit(None)

calculate_button = create_buttons("Check Hash")
calculate_button.clicked.connect(calculate_hash)
select_file_button = create_buttons("Select File")
select_file_button.clicked.connect(update_selected_file)
reset_button = create_buttons("Reset")
reset_button.clicked.connect(reset_forms)

# Initialize grid.
grid = QGridLayout()

window.setLayout(grid)

grid.addWidget(selected_file_label, 0, 0, 1, 3)
grid.addWidget(input_hash_label, 1, 0)
grid.addWidget(input_hash_box, 1, 1, 1, 2)
grid.addWidget(reset_button, 2, 0)
grid.addWidget(select_file_button, 2, 1)
grid.addWidget(calculate_button, 2, 2)

# Display window.
window.show()

# Terminate app.
sys.exit(app.exec())
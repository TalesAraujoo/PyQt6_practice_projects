# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout


# Main app objects and settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Caculator")
main_window.resize(300, 300)

# Create Objects / Widgets

calc_display = QLabel()
calc_display.setText("0")

buttons = [
    ("%",0,0), ("+/-",0,1), ("C",0,2), ("<-",0,3),
    ("7",1,0), ("8",1,1), ("9",1,2), ("/",1,3),
    ("4",2,0), ("5",2,1), ("6",2,2), ("X",2,3),
    ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3),
    (".",4,0), ("0",4,1),("=", 4,3)
    ]

grid = QGridLayout()

for btn, row, col in buttons:
    tmp_btn = QPushButton(btn)
    grid.addWidget(tmp_btn, row, col)


# Designs here
main_layout = QVBoxLayout()
main_layout.addWidget(calc_display)
main_layout.addLayout(grid)

main_window.setLayout(main_layout)


#Events


#Show / Run App
main_window.show()
app.exec()
# Import modules
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from random import choice

words = ["Hello", "Goodbye", "Japanese", "Mizu Desu", "Goku san", "whatever ever", "etc"]

def display_word1():
    word = choice(words)
    text1.setText(word)
    

def display_word2():
    word = choice(words)
    text2.setText(word)


def display_word3():
    word = choice(words)
    text3.setText(word)


def reset_texts():
    text1.setText("?")
    text2.setText("?")
    text3.setText("?")


# Main app objects and settings 
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Random Word Maker")
main_window.resize(300, 200)
 
# Create all app objects / Widgets below here
title_text = QLabel("Random Keywords")
text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

btn1 = QPushButton("Click me")
btn2 = QPushButton("Click me")
btn3 = QPushButton("Click me")
btn_reset = QPushButton("Reset")

#All Design here
master_layout = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()

row1.addWidget(title_text, alignment=Qt.AlignmentFlag.AlignCenter)

row2.addWidget(text1, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text3, alignment=Qt.AlignmentFlag.AlignCenter)

row3.addWidget(btn1, alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(btn2, alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(btn3, alignment=Qt.AlignmentFlag.AlignCenter)

row4.addWidget(btn_reset, alignment=Qt.AlignmentFlag.AlignCenter)


master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)
master_layout.addLayout(row4)

main_window.setLayout(master_layout)


# Events

btn1.clicked.connect(display_word1)
btn2.clicked.connect(display_word2)
btn3.clicked.connect(display_word3)
btn_reset.clicked.connect(reset_texts)


# Show/Run App
main_window.show()
app.exec()
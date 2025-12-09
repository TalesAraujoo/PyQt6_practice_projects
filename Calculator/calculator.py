# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QFont

result_printed = False

class CalcApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setWindowTitle("Caculator")
        self.resize(250, 300)

        self.calc_display = QLineEdit()
        self.calc_display.setReadOnly(True)
        self.calc_display.setFont(QFont("Helvetica", 25))
        self.calc_display.setText("0")

        self.calc_history_display = QLineEdit()
        self.calc_history_display.setReadOnly(True)

        self.buttons = [
            ("C",0,0), ("<-",0,1), ("%",0,2), ("/",0,3),
            ("7",1,0), ("8",1,1), ("9",1,2), ("x",1,3),
            ("4",2,0), ("5",2,1), ("6",2,2), ("-",2,3),
            ("1",3,0), ("2",3,1), ("3",3,2), ("+",3,3),
            (".",4,0), ("0",4,1),("=", 4,3)
            ]

        self.grid = QGridLayout()

        for btn, row, col in self.buttons:
            tmp_btn = QPushButton(btn)
            tmp_btn.setStyleSheet("QPushButton { font: 18pt Comic Sans MS; padding: 10px; }")
          
            tmp_btn.clicked.connect(self.button_clicked)
            self.grid.addWidget(tmp_btn, row, col)


        # Designs here
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addWidget(self.calc_history_display)
        self.main_layout.addWidget(self.calc_display)
        self.main_layout.addLayout(self.grid)

        self.setLayout(self.main_layout)


    def math_results(a, b, op):
        a = float(a)
        b = float(b)
        result = 0
        if op == '+':
            result = a+b
        elif op == '-':
            result = a-b
        elif op == 'x' or op == '*':
            result = a*b
        else:
            if b == 0:
                return 'error'
            else:
                result = a/b
        
        if result.is_integer():
            result = int(result)
            return str(result)
        else:
            return str(result)
            

    def button_clicked(self):
        global result_printed
        button = app.sender()
        text = button.text()
        current = self.calc_display.text()

        operators = {'+', '-', 'x', '/', '*'}

        # 1. Clear everything
        if text == 'C':
            self.calc_display.setText("0")
            self.calc_history_display.setText("")
            result_printed = False
            return

        # 2. Backspace
        if text == '<-':
            if result_printed or current in ("0", "Error"):
                self.calc_display.setText("0")
                result_printed = False
            elif len(current) > 1:
                self.calc_display.setText(current[:-1])
            else:
                self.calc_display.setText("0")
            return

        # 3. Equals - calculate!
        if text == '=':
            if current in ("0", "Error"):
                return
            try:
                expr = current.replace('x', '*')
                result = eval(expr)
                result_str = str(int(result)) if result.is_integer() else str(result)
                self.calc_display.setText(result_str)
                self.calc_history_display.setText(current)
                result_printed = True
            except ZeroDivisionError:
                self.calc_display.setText("Error")
                result_printed = True
            except:
                pass  # ignore invalid like "5++"
            return

        # 4. If result was shown and we press a number → start new calculation
        if result_printed and text.isdigit():
            self.calc_display.setText(text)
            result_printed = False
            return

        # 5. Get fresh display text
        current = self.calc_display.text()
        if current == "0" and text != '.':
            if text in operators:
                current = "0" + text
            else:
                current = text
        else:
            # Operator pressed
            if text in operators:
                if current and current[-1] in operators:
                    current = current[:-1] + text  # replace last operator
                else:
                    current += text
                result_printed = False
            # Decimal point
            elif text == '.':
                # Find last number part
                last_part = ""
                for c in reversed(current):
                    if c in operators:
                        break
                    last_part = c + last_part
                if '.' not in last_part:
                    current += text
            # Number or other
            else:
                if result_printed:
                    current = text
                    result_printed = False
                else:
                    current += text

        self.calc_display.setText(current if current else "0")


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key.Key_0:
            self.calc_display.setText(str(key_pressed))
        
        elif key_pressed == Qt.Key.Key_8:
            self.calc_display.setText(key_pressed)

        elif key_pressed == Qt.Key.Key_9:
            self.calc_display.setText(key_pressed)

#Show / Run App

if __name__ in "__main__":
    app = QApplication([])
    main_window = CalcApp()
    main_window.setStyleSheet("QWidget { background-color: #f0f0f8 }")
    main_window.show()
    app.exec()
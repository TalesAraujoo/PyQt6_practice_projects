from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QFont

class CalcApp(QWidget):
    def __init__(self):
        super().__init__()

        # state
        self.result_printed = False

        # window
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setWindowTitle("Calculator")
        self.resize(250, 300)

        # displays
        self.calc_display = QLineEdit()
        self.calc_display.setFont(QFont("Helvetica", 25))
        self.calc_display.setText("0")
        self.calc_display.setReadOnly(True)  # user input via buttons/keyboard

        self.calc_history_display = QLineEdit()
        self.calc_history_display.setReadOnly(True)

        # buttons layout data
        self.buttons = [
            ("C",0,0), ("<-",0,1), ("%",0,2), ("/",0,3),
            ("7",1,0), ("8",1,1), ("9",1,2), ("x",1,3),
            ("4",2,0), ("5",2,1), ("6",2,2), ("-",2,3),
            ("1",3,0), ("2",3,1), ("3",3,2), ("+",3,3),
            (".",4,0), ("0",4,1),("=", 4,3)
        ]

        # grid
        self.grid = QGridLayout()
        for label, row, col in self.buttons:
            btn = QPushButton(label)
            btn.setStyleSheet("QPushButton { font: 18pt Comic Sans MS; padding: 10px; }")
            # connect with lambda capturing current label value
            btn.clicked.connect(lambda checked, t=label: self.on_button_click(t))
            self.grid.addWidget(btn, row, col)

        # main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addWidget(self.calc_history_display)
        self.main_layout.addWidget(self.calc_display)
        self.main_layout.addLayout(self.grid)
        self.setLayout(self.main_layout)

    @staticmethod
    def math_results(a, b, op):
        a = float(a)
        b = float(b)
        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        elif op == 'x' or op == '*':
            result = a * b
        else:
            if b == 0:
                return 'error'
            result = a / b

        if float(result).is_integer():
            return str(int(result))
        else:
            return str(result)

    def on_button_click(self, text):
        """Single unified handler for both button clicks and keyboard input."""
        operators = {'+', '-', 'x', '/', '*'}

        # CLEAR
        if text == 'C':
            self.calc_display.setText("0")
            self.calc_history_display.setText("")
            self.result_printed = False
            return

        # BACKSPACE
        if text == '<-':
            current = self.calc_display.text()
            if self.result_printed or current in ("0", "Error"):
                self.calc_display.setText("0")
                self.result_printed = False
                return
            if len(current) > 1:
                self.calc_display.setText(current[:-1])
            else:
                self.calc_display.setText("0")
            return

        # EQUALS: evaluate
        if text == '=':
            current = self.calc_display.text()
            if current in ("0", "Error"):
                return
            try:
                expr = current.replace('x', '*')
                result = eval(expr)  # keep simple; we only build expr from allowed chars
                result_str = str(int(result)) if float(result).is_integer() else str(result)
                self.calc_display.setText(result_str)
                self.calc_history_display.setText(current)
                self.result_printed = True
            except ZeroDivisionError:
                self.calc_display.setText("Error")
                self.result_printed = True
            except Exception:
                # ignore invalid expressions like "5++"
                pass
            return

        # If a result was printed and we press a digit -> start new number
        if self.result_printed and text.isdigit():
            self.calc_display.setText(text)
            self.result_printed = False
            return

        # Normal input handling
        current = self.calc_display.text()
        if current == "0" and text != '.':
            if text in operators:
                current = "0" + text
            else:
                current = text
        else:
            if text in operators:
                if current and current[-1] in operators:
                    current = current[:-1] + text
                else:
                    current += text
                self.result_printed = False
            elif text == '.':
                # allow only one dot in the current number
                last_part = ""
                for c in reversed(current):
                    if c in operators:
                        break
                    last_part = c + last_part
                if '.' not in last_part:
                    current += text
            else:  # number or other
                if self.result_printed:
                    current = text
                    self.result_printed = False
                else:
                    current += text

        self.calc_display.setText(current if current else "0")

    def keyPressEvent(self, event):
        """Convert keyboard keys into the same button labels and call on_button_click."""
        key = event.key()
        ch = event.text()  # the textual representation (may be '' for non-text keys)

        # handle special keys first
        if key == Qt.Key.Key_Backspace:
            self.on_button_click('<-')
            return
        if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.on_button_click('=')
            return
        if key == Qt.Key.Key_Escape:
            self.on_button_click('C')
            return

        # map keyboard characters to our button labels
        if ch:
            # normalize '*' to 'x' so multiplication looks the same
            mapping = {'*': 'x'}
            mapped = mapping.get(ch, ch)
            # valid characters: digits, operators, dot, percent
            valid = set('0123456789.+-*/%')
            if ch in valid:
                # map '/' stays '/', '*' becomes 'x'
                if mapped == '*':
                    mapped = 'x'
                self.on_button_click(mapped)
                return

        # ignore other keys
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    main_window = CalcApp()
    main_window.setStyleSheet("QWidget { background-color: #f0f0f8 }")
    main_window.show()
    app.exec()

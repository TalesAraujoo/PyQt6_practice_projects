from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.resolve()


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_pos = None
        self.setObjectName("title_bar")
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)

        self.title_label = QLabel("Calculator")
        self.title_label.setObjectName("title_label")

        self.btn_min = QPushButton("-")
        self.btn_close = QPushButton("X")

        for btn in (self.btn_min, self.btn_close):
            btn.setFixedSize(28, 28)
            btn.setObjectName("title_button")

        self.btn_min.clicked.connect(parent.showMinimized)
        self.btn_close.clicked.connect(parent.close)

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_close)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            parent = self.window()
            parent.move(
                parent.pos()
                + event.globalPosition().toPoint()
                - self._drag_pos
            )
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()
            

class CalcApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.result_printed = False

        with open(f"{SCRIPT_DIR}/styles.qss", 'r') as file: 
            self.setStyleSheet(file.read())        
        
        #Removes Windows styling
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.title_bar = TitleBar(self)       
        self.resize(250, 300)
        
        self.calc_display = QLineEdit()
        self.calc_display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.calc_display.setReadOnly(True)
        self.calc_display.setObjectName('calc_display')
        self.calc_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.calc_display.setFont(QFont("Helvetica", 25))
        self.calc_display.setText("0")

        self.calc_history_display = QLineEdit()
        self.calc_history_display.setObjectName('history_display')
        self.calc_history_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.calc_history_display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.calc_history_display.setReadOnly(True)

        self.buttons = [
            ("C",0,0), ("<-",0,1), ("%",0,2), ("/",0,3),
            ("7",1,0), ("8",1,1), ("9",1,2), ("x",1,3),
            ("4",2,0), ("5",2,1), ("6",2,2), ("-",2,3),
            ("1",3,0), ("2",3,1), ("3",3,2), ("+",3,3),
            ("0",4,0), (".",4,2),("=", 4,3)
            ]   

        self.grid = QGridLayout()

        for btn, row, col in self.buttons:
            tmp_btn = QPushButton(btn)
            tmp_btn.clicked.connect(self.buttonPressEvent)
            
            if btn == '=':
                tmp_btn.setObjectName('equal')
            elif btn in '+-/x':
                tmp_btn.setObjectName('operator')

            if btn == '0':
                self.grid.addWidget(tmp_btn, row, col, 1, 2)
            else: 
                self.grid.addWidget(tmp_btn, row, col)

        # Designs here
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)

        self.display_container = QWidget()
        self.display_container.setObjectName('display_container')

        display_layout = QVBoxLayout()
        display_layout.setSpacing(0)
        display_layout.setContentsMargins(0,0,0,0)

        display_layout.addWidget(self.calc_history_display)
        display_layout.addWidget(self.calc_display)

        self.display_container.setLayout(display_layout)

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.display_container)
        self.main_layout.addLayout(self.grid)

        self.setLayout(self.main_layout)


    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        if text.isnumeric():
            self.input_handler(text)
        
        elif text in '+-*/xX.,=%':
            self.input_handler(text)

        elif key == 16777221 or key == 16777220:
            self.input_handler('=')
    
        elif key == 16777219:
            self.input_handler('<-')
        
        elif key == 16777216:
            self.input_handler('C')

        elif key == 16777223:
            self.input_handler('C')

    
    def buttonPressEvent(self):
        button = app.sender()
        text = button.text()
        self.input_handler(text)


    def input_handler(self,text):
    
        current = self.calc_display.text()

        operators = {'+', '-', 'x', '/', '*'}

        # 1. Clear everything
        if text == 'C':
            self.calc_display.setText("0")
            self.calc_history_display.setText("")
            self.result_printed = False
            return

        # 2. Backspace
        if text == '<-':
            if self.result_printed or current in ("0", "Error"):
                self.calc_display.setText("0")
                self.result_printed = False
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
                expr = current.lower().replace('x', '*')
                result = eval(expr)
                result_str = str(int(result)) if result.is_integer() else str(result)
                self.calc_display.setText(result_str)
                self.calc_history_display.setText(current)
                self.result_printed = True
            except ZeroDivisionError:
                self.calc_display.setText("Error")
                self.result_printed = True
            except:
                pass  # ignore invalid like "5++"
            return

        # 4. If result was shown and we press a number → start new calculation
        if self.result_printed and text.isdigit():
            self.calc_display.setText(text)
            self.result_printed = False
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
                self.result_printed = False
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
                if self.result_printed:
                    current = text
                    self.result_printed = False
                else:
                    current += text

        self.calc_display.setText(current if current else "0")


#Show / Run App
if __name__ in "__main__":
    app = QApplication([])
    main_window = CalcApp()
    main_window.show()
    app.exec()
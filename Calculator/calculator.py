# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QLineEdit

result_printed = False

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
        

def button_clicked():
    button = app.sender()
    text = button.text()
    tmp_display = calc_display.text()
    global result_printed

    operators = ['/', '*', '-', '+', 'x', 'X']

    if tmp_display == 'error':
        if text == 'C':
            calc_display.setText('0')
    
    else: 
        if text == 'C':
            calc_display.setText('0')
        elif text == '<-':
            if tmp_display == '0':
                pass
            else:
                tmp_display = tmp_display[:-1]
                calc_display.setText(tmp_display)
        elif text == '=':
            if tmp_display == '0':
                pass
            else:
                tmp_a = ''
                tmp_b = ''
                operand = ''
                result = ''
                

                for num in tmp_display:
                    
                    if not operand:
                        if num.isnumeric():
                            tmp_a += num
                        elif num == '.':
                            tmp_a += num
                        else:
                            operand = num
                    else:
                        if num.isnumeric():
                            tmp_b += num
                        elif num == '.':
                            tmp_b += num
                        else:
                            result = math_results(tmp_a, tmp_b, operand)
                            tmp_a = result
                            tmp_b = ''
                            operand = num
        
                if any(op == tmp_display[-1] for op in operators):
                    if tmp_b == '':
                        if result == '':
                            pass
                        else:
                            calc_display.setText(result)
                            result_printed = True
                else:
                    if tmp_display[-1] == '.':
                        result = math_results(tmp_a, tmp_b, operand)
                        calc_display.setText(result)  
                        result_printed = True  
                    elif tmp_display[-1].isnumeric():
                        result = math_results(tmp_a, tmp_b, operand)
                        calc_display.setText(result) 
                        result_printed = True
                    elif operand >= 1:
                        result = tmp_a
                        calc_display.setText(result)
                        result_printed = True

        else:
            if tmp_display == '0':
                if text in operators:
                    tmp_display += text
                    calc_display.setText(tmp_display)
                elif text == '.':
                    tmp_display += text
                    calc_display.setText(tmp_display)
                else:
                    tmp_display = text
                    calc_display.setText(tmp_display)
            else: 
                if text in operators:
                    if any(op == tmp_display[-1] for op in operators):
                        tmp_display = tmp_display[:-1] + text
                        calc_display.setText(tmp_display)
                    else: 
                        tmp_display += text
                        calc_display.setText(tmp_display)
                elif text == '.':
                    tmp_num = ''
                    for num in tmp_display:
                        tmp_num += num
                        if not num.isnumeric():
                            if num == '.':
                                pass
                            else:
                                tmp_num = ''

                    if '.' in tmp_num:
                        pass
                    elif tmp_display[-1] == '.':
                        pass
                    elif tmp_display[-1].isnumeric():
                        tmp_display += text
                        calc_display.setText(tmp_display)
                    else:
                        tmp_display = tmp_display + '0' + '.'
                        calc_display.setText(tmp_display)
                else:
                    if result_printed:
                        calc_display.clear()
                        calc_display.setText(text)
                        result_printed = False
                    else:
                        tmp_display += text
                        calc_display.setText(tmp_display)


# Main app objects and settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Caculator")
main_window.resize(250, 300)

# Create Objects / Widgets

calc_display = QLineEdit()
calc_display.setText("0")
calc_history_display = QLineEdit()

buttons = [
    ("C",0,0), ("<-",0,1), ("%",0,2), ("/",0,3),
    ("7",1,0), ("8",1,1), ("9",1,2), ("x",1,3),
    ("4",2,0), ("5",2,1), ("6",2,2), ("-",2,3),
    ("1",3,0), ("2",3,1), ("3",3,2), ("+",3,3),
    (".",4,0), ("0",4,1),("=", 4,3)
    ]

grid = QGridLayout()

for btn, row, col in buttons:
    tmp_btn = QPushButton(btn)
    tmp_btn.clicked.connect(button_clicked)
    grid.addWidget(tmp_btn, row, col)


# Designs here
main_layout = QVBoxLayout()
main_layout.addWidget(calc_history_display)
main_layout.addWidget(calc_display)
main_layout.addLayout(grid)

main_window.setLayout(main_layout)


#Events



#Show / Run App
main_window.show()
app.exec()
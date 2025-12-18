from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

class Testing_App(QWidget):

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowTitle("test")
        self.resize(250,250)

        main_layout = QVBoxLayout()

        btn = QPushButton()
        btn.setText('Click me')
        btn.clicked.connect(self.key_press)

        main_layout.addWidget(btn)
       
        self.setLayout(main_layout)

    
    def key_press(self):
        print('hey')
    
    def keyPressEvent(self, event):
         print(f'key: {event.key()} text: {event.text()}')
         print(f'keyT: {type(event.key())} textT: {type(event.text())}')


app = QApplication([])
window = Testing_App()
window.show()
app.exec()


from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


class TitleBar(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._drag_pos = None

        self.setFixedHeight(32)
        
        self.title_bar_layout = QHBoxLayout(self)
        self.title_bar_layout.setSpacing(0)
        self.title_bar_layout.setContentsMargins(5,0,0,0)

        self.title_bar_name = QLabel('PhotoQt - Image Editor')
        self.title_bar_name.setObjectName('title_bar_name')

        self.btn_min = QPushButton('_')
        self.btn_max = QPushButton('□')
        self.btn_close = QPushButton('X')

        self.btn_min.setObjectName('min_button')
        self.btn_max.setObjectName('max_button')
        self.btn_close.setObjectName('close_button')
        
        for btn in (self.btn_close, self.btn_max, self.btn_min):
            btn.setFixedSize(28, 28)    

        self.btn_min.clicked.connect(self.window().showMinimized)
        self.btn_max.clicked.connect(self.window().showMaximized)
        self.btn_close.clicked.connect(self.window().close)

        self.title_bar_layout.addWidget(self.title_bar_name)
        self.title_bar_layout.addStretch()
        self.title_bar_layout.addWidget(self.btn_min)
        self.title_bar_layout.addWidget(self.btn_max)
        self.title_bar_layout.addWidget(self.btn_close)


    def mousePressEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        # nothing happens if we click into a QPushButton
        child = self.childAt(event.position().toPoint())
        if isinstance(child, QPushButton):
            return

        self._drag_pos = event.globalPosition().toPoint()
        event.accept()

    
    def mouseMoveEvent(self, event):

        if (event.buttons() == Qt.MouseButton.LeftButton
            and self._drag_pos is not None
        ): 
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.window().move(self.window().pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    
    def mouseReleaseEvent(self, event):
        self._drag_pos = None



class PhotoQt(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        with open(f'{SCRIPT_DIR}/styles.qss', 'r') as file:
            self.setStyleSheet(file.read())
        
        self.resize(250,250)

        self.main_window = QVBoxLayout()
        self.main_window.setContentsMargins(0,0,0,0)
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName('title_bar')
        
        self.text_box = QLabel('Hey, testing')

        self.main_window.addWidget(self.title_bar)
        self.main_window.addWidget(self.text_box)
        self.setLayout(self.main_window)
        



if __name__ == '__main__':
    app = QApplication([])
    window = PhotoQt()
    window.show()
    app.exec()

import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QComboBox, QLabel,
    QFileDialog, QScrollArea
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class PhotoQt(QWidget):
    def __init__(self):
        super().__init__()

        # App Settings
        self.setWindowTitle('PhotoQt Image Editor')
        self.resize(800, 600)

        # Layouts
        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()
        work_area_layout = QVBoxLayout()

        # Widgets
        select_folder_btn = QPushButton('Select Folder')
        self.item_list = QListWidget()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            'Original', 'Rotate Left', 'Rotate Right', 'Mirror',
            'Sharpen', 'Black and White', 'Enhance Color', 'Increase Contrast'
        ])

        # Edit buttons
        self.btn_left = QPushButton('Rotate Left')
        self.btn_right = QPushButton('Rotate Right')
        self.btn_mirror = QPushButton('Mirror')
        self.btn_sharpen = QPushButton('Sharpen')
        self.btn_bw = QPushButton('Black and White')
        self.btn_color = QPushButton('Enhance Color')
        self.btn_contrast = QPushButton('Increase Contrast')

        # Image display label (scaled)
        self.image_label = QLabel('No image selected')
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 400)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        # Scroll area for large images
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)

        # Current state
        self.working_directory = ""
        self.current_image_path = None
        self.original_pixmap = None
        self.current_pixmap = None

        # Sidebar layout
        sidebar_layout.addWidget(select_folder_btn)
        sidebar_layout.addWidget(QLabel("Images in folder:"))
        sidebar_layout.addWidget(self.item_list)
        sidebar_layout.addWidget(QLabel("Quick Filter:"))
        sidebar_layout.addWidget(self.filter_combo)
        sidebar_layout.addWidget(QLabel("Manual Edits:"))
        sidebar_layout.addWidget(self.btn_left)
        sidebar_layout.addWidget(self.btn_right)
        sidebar_layout.addWidget(self.btn_mirror)
        sidebar_layout.addWidget(self.btn_sharpen)
        sidebar_layout.addWidget(self.btn_bw)
        sidebar_layout.addWidget(self.btn_color)
        sidebar_layout.addWidget(self.btn_contrast)
        sidebar_layout.addStretch()

        # Work area
        work_area_layout.addWidget(scroll_area)

        # Main layout (20% sidebar, 80% work area)
        main_layout.addLayout(sidebar_layout, 20)
        main_layout.addLayout(work_area_layout, 80)

        self.setLayout(main_layout)

        # Connections
        select_folder_btn.clicked.connect(self.get_work_directory)
        self.item_list.itemClicked.connect(self.load_image)
        self.filter_combo.currentTextChanged.connect(self.apply_quick_filter)

        # Button connections
        self.btn_left.clicked.connect(lambda: self.apply_transformation('rotate_left'))
        self.btn_right.clicked.connect(lambda: self.apply_transformation('rotate_right'))
        self.btn_mirror.clicked.connect(lambda: self.apply_transformation('mirror'))
        self.btn_sharpen.clicked.connect(lambda: self.apply_transformation('sharpen'))
        self.btn_bw.clicked.connect(lambda: self.apply_transformation('black_white'))
        self.btn_color.clicked.connect(lambda: self.apply_transformation('enhance_color'))
        self.btn_contrast.clicked.connect(lambda: self.apply_transformation('contrast'))

    @staticmethod
    def filter_files(files, extensions):
        return [f for f in files if any(f.lower().endswith(ext) for ext in extensions)]

    def get_work_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if not directory:
            return

        self.working_directory = directory
        extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg']
        filenames = self.filter_files(os.listdir(directory), extensions)
        print(os.listdir(directory))

        self.item_list.clear()
        for filename in sorted(filenames):
            self.item_list.addItem(filename)

        self.image_label.setText("Select an image from the list")

    def load_image(self, item):
        if not self.working_directory:
            return

        filename = item.text()
        self.current_image_path = os.path.join(self.working_directory, filename)

        pixmap = QPixmap(self.current_image_path)
        if pixmap.isNull():
            self.image_label.setText("Failed to load image")
            return

        self.original_pixmap = pixmap
        self.current_pixmap = pixmap.copy()
        self.display_image()

        # Reset filter combo to Original
        self.filter_combo.blockSignals(True)
        self.filter_combo.setCurrentText('Original')
        self.filter_combo.blockSignals(False)

    def display_image(self):
        if self.current_pixmap:
            scaled = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_image()  # Re-scale image when window resizes

    def apply_quick_filter(self, filter_name):
        if not self.original_pixmap:
            return
        self.current_pixmap = self.original_pixmap.copy()
        self.apply_transformation(filter_name.replace(' ', '_').lower())

    def apply_transformation(self, transform_type):
        if not self.current_pixmap:
            return

        pixmap = self.current_pixmap

        if transform_type == 'rotate_left':
            pixmap = pixmap.transformed(Qt.TransformationMode.RotateLeft90)
        elif transform_type == 'rotate_right':
            pixmap = pixmap.transformed(Qt.TransformationMode.RotateRight90)
        elif transform_type == 'mirror':
            pixmap = pixmap.transformed(Qt.TransformationMode.Rotate180).transformed(Qt.TransformationMode.FlipHorizontal)
            # Or simpler: pixmap = pixmap.mirrored(True, False)
            pixmap = pixmap.mirrored(True, False)
        # Note: Sharpen, B&W, Color enhance, Contrast require QImage + filters
        # These are more complex and need PIL or manual pixel ops for full effect
        # For now, we'll leave them as placeholders or use basic approximations

        self.current_pixmap = pixmap
        self.display_image()


if __name__ == '__main__':
    app = QApplication([])
    window = PhotoQt()
    window.show()
    app.exec()
#Import Modules
import os
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QComboBox, QLabel, QFileDialog
)


class PhotoQt(QWidget):

    def __init__(self):
        super().__init__()
        self.image = None
        self.original_img = None
        self.filename = None
        self.pathdir_name = None
        self.save_folder = 'edits/'
        self.TMP_DIRECTORY = os.path.join(Path(__file__).parent.resolve(), 'temp') 
        self.working_directory = ""
        
        #App Settings
        self.setWindowTitle('PhotoQt Image Editor')
        self.resize(400, 400)


        #All app widgets/objects
        main_row = QHBoxLayout()
        sidebar_menu = QVBoxLayout()
        work_area = QVBoxLayout()

        select_folder = QPushButton('Select Folder')
        self.item_list = QListWidget()
        self.image_left = QPushButton('Left')
        self.image_right = QPushButton('Right')
        self.image_mirror = QPushButton('Mirror')
        self.image_sharpness = QPushButton('Sharpness')
        self.image_bw = QPushButton('Black and White')
        self.image_color = QPushButton('Color')
        self.image_contrast = QPushButton('Contrast')
        self.image_blur = QPushButton('Blur')
        self.save_edited_img = QPushButton('Save')

        self.combo_box = QComboBox()
        self.combo_box.addItem('Original')
        self.combo_box.addItem('Left')
        self.combo_box.addItem('Right')
        self.combo_box.addItem('Mirror')
        self.combo_box.addItem('Sharpness')
        self.combo_box.addItem('Black and White')
        self.combo_box.addItem('Color')
        self.combo_box.addItem('Contrast')
        self.combo_box.addItem('Blur')

        self.image_edit_area = QLabel('Editting here')
        self.image_edit_area.setMinimumSize(400,400)
        self.image_edit_area.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #App Design 
        sidebar_menu.addWidget(select_folder)
        sidebar_menu.addWidget(self.item_list)
        sidebar_menu.addWidget(self.combo_box)
        sidebar_menu.addWidget(self.image_left)
        sidebar_menu.addWidget(self.image_right)
        sidebar_menu.addWidget(self.image_mirror)
        sidebar_menu.addWidget(self.image_sharpness)
        sidebar_menu.addWidget(self.image_bw)
        sidebar_menu.addWidget(self.image_color)
        sidebar_menu.addWidget(self.image_contrast)
        sidebar_menu.addWidget(self.image_blur)
        sidebar_menu.addWidget(self.save_edited_img)
        
        work_area.addWidget(self.image_edit_area)

        main_row.addLayout(sidebar_menu, 20)
        main_row.addLayout(work_area, 80)

        self.setLayout(main_row)

        self.item_list.currentRowChanged.connect(self.display_image)
        self.combo_box.currentIndexChanged.connect(self.on_combobox_change)
        select_folder.clicked.connect(self.getWorkDirectory)
        self.image_bw.clicked.connect(self.black_white)
        self.image_left.clicked.connect(self.rotate_left)
        self.image_right.clicked.connect(self.rotate_right)    
        self.image_mirror.clicked.connect(self.mirror)
        self.image_sharpness.clicked.connect(self.sharpness)
        self.image_color.clicked.connect(self.color)
        self.image_contrast.clicked.connect(self.contrast)
        self.image_blur.clicked.connect(self.blur)
        self.save_edited_img.clicked.connect(self.save_img_edited)

    #get only image files from the selected directory
    def filter_images(self, files, extensions):
        results = []
        
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    results.append(file)

        return results
    

    def getWorkDirectory(self):
        
        self.working_directory = QFileDialog.getExistingDirectory()
        if not self.working_directory:
            return

        extensions = ['.png', '.jpeg', '.svg']
        filenames = self.filter_images(os.listdir(self.working_directory), extensions)
        self.item_list.clear()

        for filename in filenames:
            self.item_list.addItem(filename)

    
    def load_image(self, filename):
        self.filename = filename
        self.pathdir_name = os.path.join(self.working_directory, self.filename)
        self.image = Image.open(self.pathdir_name)
        self.original_img = self.image.copy()


    def save_image(self):
        path = os.path.join(self.working_directory, self.save_folder)
        if not os.path.exists(path) or os.path.isdir(path):
            os.mkdir(path)

        full_dir_name = os.path.join(path, self.filename)
        self.image.save(full_dir_name)


    def save_tmp_file(self):
        if not (os.path.exists(self.TMP_DIRECTORY)):
            os.mkdir(self.TMP_DIRECTORY)

        full_dir_name = os.path.join(self.TMP_DIRECTORY, self.filename)
        self.image.save(full_dir_name)
            

    def show_image(self, path):
        self.image_edit_area.hide()
        image = QPixmap(path)
        width, height = self.image_edit_area.width(), self.image_edit_area.height()
        image = image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)

        self.image_edit_area.setPixmap(image)
        self.image_edit_area.show()

    
    def display_image(self):
        if self.item_list.currentRow() >= 0:
            filename = self.item_list.currentItem().text()
            self.load_image(filename)
            self.show_image(self.pathdir_name)


    def black_white(self):
        if self.image:
            self.image = self.image.convert("L")
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            
            self.show_image(path)


    def rotate_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)

            self.show_image(path)


    def rotate_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def mirror(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def sharpness(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def color(self):
        if self.image:
            self.image = ImageEnhance.Color(self.image).enhance(1.2)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def contrast(self):
        if self.image:
            self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.save_tmp_file()
            path = os.path.join(self.TMP_DIRECTORY, self.filename)
            self.show_image(path)


    def on_combobox_change(self):
        
        selected_text = self.combo_box.currentText()

        if selected_text == 'Original':
            if self.image:
                self.image = self.original_img
                path = os.path.join(self.working_directory, self.filename)            
                self.show_image(path)
        elif selected_text == 'Left':
            self.rotate_left()
        elif selected_text == 'Right':
            self.rotate_right()
        elif selected_text == 'Mirror':
            self.mirror()
        elif selected_text == 'Sharpness':
            self.sharpness()
        elif selected_text == 'Black and White':
            self.black_white()
        elif selected_text == 'Color':
            self.color()
        elif selected_text == 'Contrast':
            self.contrast()
        elif selected_text == 'Blur':
            self.blur()


    def save_img_edited(self):
        path = os.path.join(self.working_directory, self.filename)
        self.image.save(path)


app = QApplication([])
window = PhotoQt()
window.show()
app.exec()
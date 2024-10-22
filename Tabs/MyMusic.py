import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QLineEdit, QTableWidget, 
                             QTableWidgetItem,QHBoxLayout, QPushButton, QFileDialog)


class MyMusic(QtWidgets.QWidget):  # This is the music tab
    play = QtCore.pyqtSignal(object)
    addFavourite = QtCore.pyqtSignal(object)
    addToCollection = QtCore.pyqtSignal(object, bool)
    playlist_added = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MyMusic, self).__init__(*args, **kwargs)

        self.dirs = set()
        self.music_files = list()
        self.file_path = list()

        self.initUI()

    def initUI(self):
        self.setLayout(QtWidgets.QVBoxLayout())

        self.setObjectName("MyFile")

        #tạo bảng
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Filename", "Type", "Size", "Publish", "Delete"])

        # Tạo ô nhập để nhập tên file cần tìm
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên file để tìm...")
        self.search_layout.addWidget(self.search_input)
        self.search_input.textChanged.connect(self.search_file)


        # Tạo nút "Upload File"
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)

        self.layout().setSpacing(20)
        self.layout().setContentsMargins(*[10]*4)
        self.layout().addLayout(self.search_layout)
        self.layout().addWidget(self.table)
        self.layout().addWidget(self.upload_button)

    def search(self, string):

        if not string:
            self.stack_view.setCurrentIndex(0)
            return

        if self.stack_view.currentIndex() == 0:
            self.stack_view.setCurrentIndex(1)

        widgets = self.view.widgets()

        self.search_display_widget.removeTileParent()
        self.search_display_widget.deleteAll()
        for tile in widgets:
            if tile.getTitle().lower().startswith(string.lower()):
                self.search_display_widget.addMusicTile(tile)


    def addSearchDir(self, dir):
        self.dirs.add(dir)

    def deleteSearchDir(self, dirs):
        try:
            self.dirs.remove(dirs)

        except KeyError:
            pass

        self.loadFiles()

    def add_table_row(self, file_name, file_type, file_size):
        # Lấy số hàng hiện tại để thêm hàng mới
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Tạo các ô cho cột "Tên file", "Loại file", và "Kích thước"
        self.table.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(file_type))
        self.table.setItem(row_position, 2, QTableWidgetItem(file_size))
        
        # Tạo nút Publish cho cột Publish
        publish_button = QPushButton('Publish')
        publish_button.clicked.connect(lambda: self.publish_file(file_name))
        # Tạo nút Publish cho cột Delete
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda _, row=row_position: self.delete_row(row))
        
        self.table.setCellWidget(row_position, 4, delete_button)
        self.table.setCellWidget(row_position, 3, publish_button)

    def upload_file(self):
        # Mở hộp thoại để chọn file
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Chọn file để upload", "", "All Files (*.*)")

        # Nếu người dùng chọn file
        if file_paths:
            for file_path in file_paths:
                # Lấy thông tin file
                file_name = os.path.basename(file_path)
                file_size = self.get_file_size(file_path)
                file_type = self.get_file_type(file_name)

                # Thêm file vào bảng
                self.add_table_row(file_name, file_type, file_size)

    def delete_row(self, row_position):
        # Xóa hàng tương ứng
        self.table.removeRow(row_position)
        print(f"Đã xóa hàng {row_position}")

    def get_file_size(self, file_path):
        # Lấy kích thước file theo KB, MB, GB
        size = os.path.getsize(file_path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 ** 2:
            return f"{size // 1024} KB"
        elif size < 1024 ** 3:
            return f"{size // (1024 ** 2)} MB"
        else:
            return f"{size // (1024 ** 3)} GB"

    def get_file_type(self, file_name):
        # Lấy loại file từ đuôi mở rộng
        return file_name.split('.')[-1].upper() + " File"
    
    def publish_file(self, file_name):
        print(f'Publishing {file_name}')
    def search_file(self):
        # Lấy tên file cần tìm từ ô nhập
        search_text = self.search_input.text()
        print(search_text)
        # Tìm kiếm file trong bảng
        for row in range(self.table.rowCount()):
            file_name = self.table.item(row, 0).text()
            # Kiểm tra xem file có chứa chuỗi tìm kiếm không
            if search_text in file_name:
                # Hiển thị hàng nếu tìm thấy
                self.table.setRowHidden(row, False)
            else:
                # Ẩn các hàng không khớp
                self.table.setRowHidden(row, True)

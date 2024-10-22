import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import Paths
from VerticalTabs import TabWidget
from Tabs import MyMusic, Favourites, MyCollections
class FileUploadWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập layout chính cho widget
        self.layout = QVBoxLayout()
        

        #Tạo frame
        self.windowFrame = QtWidgets.QWidget(objectName="WindowFrame")
        self.windowFrame.setLayout(QtWidgets.QHBoxLayout())
        self.windowFrame.setFixedHeight(50)
        self.windowFrame.layout().setSpacing(10)

        # Tạo tab
        self.tabWidget = TabWidget()
        self.myMusic = MyMusic.MyMusic()
        self.favourites = Favourites.Favourite()
        self.musicCollections = MyCollections.MyCollection()
        # Tạo sideTab (verticalTabs)
        self.tabWidget.addTab(self.myMusic, "My File", QtGui.QIcon(Paths.MUSIC))
        self.tabWidget.addTab(self.favourites, "Public File", QtGui.QIcon(Paths.PUBLIC))
        self.tabWidget.addTab(self.musicCollections, "Collections", QtGui.QIcon(Paths.PUBLIC))

        self.windowFrame.layout().setStretch(0, 1)
        

        self.layout.addWidget(self.windowFrame)
        self.layout.addWidget(self.tabWidget)
        # self.layout.addWidget(self.upload_button)

        self.setLayout(self.layout)

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
        
        # Thêm nút vào cột 4 của bảng
        self.table.setCellWidget(row_position, 3, publish_button)

    def publish_file(self, file_name):
        print(f'Publishing {file_name}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileUploadWidget()
    window.setWindowTitle('File Upload Table')
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())

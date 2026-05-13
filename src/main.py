import os
from mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import apply_stylesheet


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    os.environ["QT_AUTOSCREENSCALE_FACTOR"] = "1"

    app = QApplication([])
    apply_stylesheet(app, theme="dark_red.xml")
    
    window = MyWindow()
    window.showMaximized()
    app.exec()
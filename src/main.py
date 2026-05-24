import os
from mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import apply_stylesheet
from datetime import datetime
import queue
import threading

from DataManager import DataManager
from receiver import run_receiver
from config import SERIAL_PORT, BAUD_RATE, SOURCE_SYSTEM
from Logger import MyLogger


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    os.environ["QT_AUTOSCREENSCALE_FACTOR"] = "1"


    data_queue = queue.Queue()

    maintenant = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier_booster = "booster_" + maintenant
    nom_fichier_sustainer = "sustainer_" + maintenant

    logger_booster = MyLogger(nom_fichier_booster)
    logger_sustainer = MyLogger(nom_fichier_sustainer)

    data_manager = DataManager(logger_sustainer, logger_booster, data_queue)


    thread = threading.Thread(target=run_receiver(serial_port=SERIAL_PORT, source_system=SOURCE_SYSTEM, 
                                                  baud_rate=BAUD_RATE, data_queue=data_queue), daemon=True)
    thread.start()


    app = QApplication([])
    apply_stylesheet(app, theme="dark_red.xml")
    
    window = MyWindow()
    window.showMaximized()
    app.exec()

import os
from mainWindow import PageDonnees, Header, PageBelle
from PyQt6.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout
from qt_material import apply_stylesheet
from datetime import datetime
import queue
import threading

from DataManager import DataManager
from receiver import run_receiver
from config import SERIAL_PORT, BAUD_RATE, SOURCE_SYSTEM
from Logger import MyLogger


class MyWindow(QMainWindow):
    def __init__(self, logger_sustainer, logger_booster, stop, thread):
        super().__init__()
        obj_path = os.path.join(os.path.dirname(__file__), "assets", "fusee.obj")

        self.setFixedSize(1280, 720)

        self.logger_booster = logger_booster
        self.logger_sustainer = logger_sustainer
        self.thread = thread
        self.stop = stop

        self.page_booster = PageDonnees()
        self.page_sustainer = PageDonnees()
        self.page_belle_booster   = PageBelle(obj_path)
        self.page_belle_sustainer = PageBelle(obj_path)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.page_booster, "Booster (Données)")
        self.tabs.addTab(self.page_sustainer, "Sustainer (Données)")
        self.tabs.addTab(self.page_belle_booster,   "Booster")
        self.tabs.addTab(self.page_belle_sustainer, "Sustainer")

        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(Header("Ground Station"))
        layout.addWidget(self.tabs)
        container.setLayout(layout)

        self.setCentralWidget(container)

    def closeEvent(self, event):
        self.stop.set()
        self.thread.join()
        self.logger_booster.stop()
        self.logger_sustainer.stop()
        event.accept()



if __name__ == "__main__":
    os.environ["QT_AUTOSCREENSCALE_FACTOR"] = "1"

    data_queue = queue.Queue()


    # Création des fichiers

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    maintenant = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier_booster = os.path.join(logs_dir, "booster_" + maintenant + ".csv")
    nom_fichier_sustainer = os.path.join(logs_dir, "sustainer_" + maintenant + ".csv")


    # Création des instances
    
    logger_booster = MyLogger(nom_fichier_booster)
    logger_sustainer = MyLogger(nom_fichier_sustainer)


    # Création du thread de la fonction receiver

    stop = threading.Event()

    thread = threading.Thread(target=run_receiver, args=(SERIAL_PORT, SOURCE_SYSTEM, BAUD_RATE, data_queue, stop))
    thread.start()


    # Création de l'interface

    app = QApplication([])
    apply_stylesheet(app, theme="dark_red.xml")
    
    window = MyWindow(logger_booster, logger_sustainer, stop, thread)
    window.showMaximized()


    # Création de Data Manager

    data_manager = DataManager(logger_sustainer, logger_booster, data_queue)


    data_manager.signal_booster.connect(window.page_booster.update_dico)
    data_manager.signal_sustainer.connect(window.page_sustainer.update_dico)
    data_manager.signal_freq.connect(window.page_booster.update_freq)
    data_manager.signal_freq.connect(window.page_sustainer.update_freq)
    data_manager.signal_booster.connect(window.page_belle_booster.update_dico)
    data_manager.signal_sustainer.connect(window.page_belle_sustainer.update_dico)

    app.exec()

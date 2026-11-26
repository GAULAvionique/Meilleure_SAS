import os
import platform

from pathlib import Path
from datetime import datetime
import queue
import threading
from collections.abc import Sequence
import argparse

from logging import getLevelNamesMapping
import logging


import OpenGL
from PyQt6 import QtGui
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout

import pyqtgraph as pg

from qt_material import apply_stylesheet

from lib.mainwindow import PageDonnees, Header, PageBelle
from lib.data_manager import DataManager
from lib.receiver import run_receiver
from lib.config import SERIAL_PORT, BAUD_RATE, SOURCE_SYSTEM
from lib.logger import MyLogger

from lib.server_connection import ServerConnection


OpenGL.USE_ACCELERATE = False
pg.setConfigOption('useOpenGL', True)

if platform == 'Linux':
    os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["MESA_GL_VERSION_OVERRIDE"] = "3.3"


fmt = QtGui.QSurfaceFormat()
fmt.setRenderableType(QtGui.QSurfaceFormat.RenderableType.OpenGL)
fmt.setProfile(QtGui.QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
fmt.setDepthBufferSize(24)
QtGui.QSurfaceFormat.setDefaultFormat(fmt)

BASE_DIR = Path(__file__).resolve().parent


# Gets the logger
logger = logging.getLogger(__name__)
class MyWindow(QMainWindow):
    def __init__(self, logger_sustainer, logger_booster, stop, thread):
        super().__init__()
        obj_path = str(BASE_DIR / 'assets' / 'fusee.obj')

        self.showFullScreen()
        #self.setFixedSize(1280, 720)

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

def _on_samples():
    pass


def main(argv: Sequence[str] | None = None) -> int:
    """
    The entry point function of the SAS
    """

    # Just the parser, kinda represents the program in CLI
    parser = argparse.ArgumentParser(
        prog="./run.sh",
        description="Runs the GAUL SAS."
    )

    ## Logging
    # Log level
    log_levels = list(getLevelNamesMapping().keys())
    parser.add_argument(
        "--log-level", "-L",
        type = str,
        default = "INFO",
        choices = log_levels,
        help =
        """
        Sets the log level. Only logs of the same level and higher are logged.
        Must be uppercase only.
        (Default: INFO)
        """
    )
    parser.add_argument(
        "--log-file",
        type = Path,
        help =
        """
        Sets the logging to be written to file instead of terminal.
        """
    )

    ## TelemetryServer
    # Address
    parser.add_argument(
        "--server-addr",
        type = str,
        default = "127.0.0.1",
        help =
        """
        Sets the address the SAS connects to.
        (Default: 127.0.0.1)
        """
    )
    # Port
    parser.add_argument(
        "--server-port",
        type = int,
        default = 42069, # so stupid, I love it
        help =
        """
        Sets the port the SAS connects to.
        (Default: 42069)
        """
    )

    args = parser.parse_args(argv)
    logging.basicConfig(
                level=args.log_level,
                filename=args.log_file,
                format="%(asctime)s %(levelname)-8s %(threadName)s %(name)s: %(message)s"
            )

    server_conn = ServerConnection("127.0.0.1", 42069, _on_samples)
    server_conn.start()

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
    QtGui.QSurfaceFormat.setDefaultFormat(QtGui.QSurfaceFormat())

    app = QApplication([])
    apply_stylesheet(app, theme="dark_red.xml")

    window = MyWindow(logger_booster, logger_sustainer, stop, thread)

    # Création de Data Manager
    data_manager = DataManager(logger_sustainer, logger_booster, data_queue)
    window.data_manager = data_manager

    data_manager.signal_booster.connect(window.page_booster.update_dico)
    data_manager.signal_sustainer.connect(window.page_sustainer.update_dico)
    data_manager.signal_freq.connect(window.page_booster.update_freq)
    data_manager.signal_freq.connect(window.page_sustainer.update_freq)
    data_manager.signal_booster.connect(window.page_belle_booster.update_dico)
    data_manager.signal_sustainer.connect(window.page_belle_sustainer.update_dico)

    QTimer.singleShot(100,window.showMaximized)

    # the code stops here until app.exec() returns
    app.exec()
    server_conn.stop()
    server_conn.join()

if __name__ == "__main__":
    raise SystemExit(main())

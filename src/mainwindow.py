from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
import sys


app = QApplication(sys.argv)
fenetre = QWidget()


layout_principal = QVBoxLayout()
layout_gps = QHBoxLayout()
layout_orientation = QHBoxLayout()
layout_system = QHBoxLayout()
layout_imu = QHBoxLayout()


layout_principal.addWidget(QLabel("Header"))
layout_principal.addWidget(QLabel("Section 1"))
layout_principal.addWidget(QLabel("Section 2"))


fenetre.setLayout(layout_principal)
fenetre.setWindowTitle("Ground Station")
fenetre.show()
sys.exit(app.exec())
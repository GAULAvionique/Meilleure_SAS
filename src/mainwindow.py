from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QGroupBox,
    QScrollArea, QSizePolicy, 
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont
import pyqtgraph as pg
import numpy as np
import os


MAX_GRAPH_POINTS = 5000

class Header(QWidget):
    def __init__(self, titre="Ground Station"):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(6, 3, 6, 3)

        label_titre = QLabel(titre)
        label_titre.setStyleSheet("font-size: 20px; font-weight: bold;")

        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_gaul.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaledToHeight(50, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("GAUL")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(label_titre)
        layout.addStretch()
        layout.addWidget(logo_label)
        self.setLayout(layout)



class PageDonnees(QWidget):
    def __init__(self):
        super().__init__()

        self.label_mission_state    = QLabel("--")
        self.label_battery          = QLabel("-- V")
        self.label_temp             = QLabel("-- °C")
        self.label_pressure         = QLabel("-- kPa")
        self.label_freq_msg         = QLabel("-- Hz")

        self.label_lat              = QLabel("-- °")
        self.label_lon              = QLabel("-- °")
        self.label_gps_alt          = QLabel("-- m")
        self.label_vel              = QLabel("-- m/s")
        self.label_cog              = QLabel("-- °")
        self.label_satellites_nb    = QLabel("--")
        self.label_gps_fix          = QLabel("--")

        self.label_kalman_z         = QLabel("-- m")
        self.label_kalman_v         = QLabel("-- m/s")

        self.label_roll             = QLabel("-- °")
        self.label_pitch            = QLabel("-- °")
        self.label_yaw              = QLabel("-- °")

        self.label_imu_acc_x            = QLabel("-- m/s²")
        self.label_imu_acc_y            = QLabel("-- m/s²")
        self.label_imu_acc_z            = QLabel("-- m/s²")
        self.label_imu_acc_vertical     = QLabel("-- m/s²")
        self.label_imu_gyro_x           = QLabel("-- °/s")
        self.label_imu_gyro_y           = QLabel("-- °/s")
        self.label_imu_gyro_z           = QLabel("-- °/s")
        self.label_imu_mag_x            = QLabel("-- µT")
        self.label_imu_mag_y            = QLabel("-- µT")
        self.label_imu_mag_z            = QLabel("-- µT")

        self.label_highg_acc_x          = QLabel("-- m/s²")
        self.label_highg_acc_y          = QLabel("-- m/s²")
        self.label_highg_acc_z          = QLabel("-- m/s²")
        self.label_highg_acc_vertical   = QLabel("-- m/s²")

        self.label_flag_idefix_ok       = QLabel("● IDEFIX")
        self.label_flag_bt_ok           = QLabel("● BT")
        self.label_flag_flash_ok        = QLabel("● FLASH")
        self.label_flag_sd_ok           = QLabel("● SD")
        self.label_flag_temp_ok         = QLabel("● TEMP")
        self.label_flag_highg_ok        = QLabel("● HIGH-G")
        self.label_flag_gps_ok          = QLabel("● GPS")
        self.label_flag_baro_ok         = QLabel("● BARO")
        self.label_flag_imu_ok          = QLabel("● IMU")
        self.label_flag_radio_ok        = QLabel("● RADIO")
        self.label_flag_pyros_armed_ok  = QLabel("● PYROS ARMED")
        self.label_flag_pyro1_conn      = QLabel("● PYRO1 CONN")
        self.label_flag_pyro2_conn      = QLabel("● PYRO2 CONN")
        self.label_flag_pyro3_conn      = QLabel("● PYRO3 CONN")
        self.label_flag_pyro4_conn      = QLabel("● PYRO4 CONN")

        self.label_flag_pyros_armed         = QLabel("● PYROS ARMED")
        self.label_flag_pyro1_fired         = QLabel("● PYRO1 FIRED")
        self.label_flag_pyro2_fired         = QLabel("● PYRO2 FIRED")
        self.label_flag_pyro3_fired         = QLabel("● PYRO3 FIRED")
        self.label_flag_pyro4_fired         = QLabel("● PYRO4 FIRED")
        self.label_flag_apogee_detected     = QLabel("● APOGEE")
        self.label_flag_main_deployed       = QLabel("● MAIN")
        self.label_flag_drogue_deployed     = QLabel("● DROGUE")
        self.label_flag_mach_lock_enabled   = QLabel("● MACH LOCK")

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(8)

        rangee1 = QHBoxLayout()
        rangee1.addWidget(self._groupe_etat_general())
        rangee1.addWidget(self._groupe_orientation())
        rangee1.addWidget(self._groupe_kalman())
        rangee1.addWidget(self._groupe_highg())
        layout_principal.addLayout(rangee1)

        rangee2 = QHBoxLayout()
        rangee2.addWidget(self._groupe_imu())
        rangee2.addWidget(self._groupe_gps())
        layout_principal.addLayout(rangee2)

        layout_principal.addWidget(self._groupe_system_states())
        layout_principal.addWidget(self._groupe_event_states())
        layout_principal.addStretch()

        contenu = QWidget()
        contenu.setLayout(layout_principal)

        scroll = QScrollArea()
        scroll.setWidget(contenu)
        scroll.setWidgetResizable(True)

        layout_root = QVBoxLayout()
        layout_root.setContentsMargins(0, 0, 0, 0)
        layout_root.addWidget(scroll)
        self.setLayout(layout_root)


    def _groupe_etat_general(self):
        groupe = QGroupBox("Général")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Mission :"),   0, 0); layout.addWidget(self.label_mission_state, 0, 1)
        layout.addWidget(QLabel("Batterie :"),  1, 0); layout.addWidget(self.label_battery,       1, 1)
        layout.addWidget(QLabel("Temp :"),      2, 0); layout.addWidget(self.label_temp,           2, 1)
        layout.addWidget(QLabel("Pression :"),  3, 0); layout.addWidget(self.label_pressure,       3, 1)
        layout.addWidget(QLabel("Fréq. msg :"), 4, 0); layout.addWidget(self.label_freq_msg,       4, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_gps(self):
        groupe = QGroupBox("GPS")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Latitude :"),   0, 0); layout.addWidget(self.label_lat,           0, 1)
        layout.addWidget(QLabel("Longitude :"),  1, 0); layout.addWidget(self.label_lon,           1, 1)
        layout.addWidget(QLabel("Altitude :"),   2, 0); layout.addWidget(self.label_gps_alt,       2, 1)
        layout.addWidget(QLabel("Vitesse :"),    3, 0); layout.addWidget(self.label_vel,           3, 1)
        layout.addWidget(QLabel("Cap :"),        4, 0); layout.addWidget(self.label_cog,           4, 1)
        layout.addWidget(QLabel("Satellites :"), 5, 0); layout.addWidget(self.label_satellites_nb, 5, 1)
        layout.addWidget(QLabel("Fix :"),        6, 0); layout.addWidget(self.label_gps_fix,       6, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_kalman(self):
        groupe = QGroupBox("Kalman")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Altitude :"), 0, 0); layout.addWidget(self.label_kalman_z, 0, 1)
        layout.addWidget(QLabel("Vitesse :"),  1, 0); layout.addWidget(self.label_kalman_v, 1, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_orientation(self):
        groupe = QGroupBox("Orientation")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Roll :"),  0, 0); layout.addWidget(self.label_roll,  0, 1)
        layout.addWidget(QLabel("Pitch :"), 1, 0); layout.addWidget(self.label_pitch, 1, 1)
        layout.addWidget(QLabel("Yaw :"),   2, 0); layout.addWidget(self.label_yaw,   2, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_imu(self):
        groupe = QGroupBox("IMU")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Acc X :"),     0, 0); layout.addWidget(self.label_imu_acc_x,        0, 1)
        layout.addWidget(QLabel("Acc Y :"),     1, 0); layout.addWidget(self.label_imu_acc_y,        1, 1)
        layout.addWidget(QLabel("Acc Z :"),     2, 0); layout.addWidget(self.label_imu_acc_z,        2, 1)
        layout.addWidget(QLabel("Acc vert. :"), 3, 0); layout.addWidget(self.label_imu_acc_vertical, 3, 1)
        layout.addWidget(QLabel("Gyro X :"),    4, 0); layout.addWidget(self.label_imu_gyro_x,       4, 1)
        layout.addWidget(QLabel("Gyro Y :"),    5, 0); layout.addWidget(self.label_imu_gyro_y,       5, 1)
        layout.addWidget(QLabel("Gyro Z :"),    6, 0); layout.addWidget(self.label_imu_gyro_z,       6, 1)
        layout.addWidget(QLabel("Mag X :"),     7, 0); layout.addWidget(self.label_imu_mag_x,        7, 1)
        layout.addWidget(QLabel("Mag Y :"),     8, 0); layout.addWidget(self.label_imu_mag_y,        8, 1)
        layout.addWidget(QLabel("Mag Z :"),     9, 0); layout.addWidget(self.label_imu_mag_z,        9, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_highg(self):
        groupe = QGroupBox("High-G")
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        layout.addWidget(QLabel("Acc X :"),     0, 0); layout.addWidget(self.label_highg_acc_x,        0, 1)
        layout.addWidget(QLabel("Acc Y :"),     1, 0); layout.addWidget(self.label_highg_acc_y,        1, 1)
        layout.addWidget(QLabel("Acc Z :"),     2, 0); layout.addWidget(self.label_highg_acc_z,        2, 1)
        layout.addWidget(QLabel("Acc vert. :"), 3, 0); layout.addWidget(self.label_highg_acc_vertical, 3, 1)
        groupe.setLayout(layout)
        return groupe

    def _groupe_system_states(self):
        groupe = QGroupBox("System States")
        groupe.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        for label in [
            self.label_flag_idefix_ok, self.label_flag_bt_ok,
            self.label_flag_flash_ok,  self.label_flag_sd_ok,
            self.label_flag_temp_ok,   self.label_flag_highg_ok,
            self.label_flag_gps_ok,    self.label_flag_baro_ok,
            self.label_flag_imu_ok,    self.label_flag_radio_ok,
            self.label_flag_pyros_armed_ok, self.label_flag_pyro1_conn,
            self.label_flag_pyro2_conn,     self.label_flag_pyro3_conn,
            self.label_flag_pyro4_conn,
        ]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            layout.addWidget(label)
        groupe.setLayout(layout)
        return groupe

    def _groupe_event_states(self):
        groupe = QGroupBox("Event States")
        groupe.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(3)
        for label in [
            self.label_flag_pyros_armed,
            self.label_flag_pyro1_fired,     self.label_flag_pyro2_fired,
            self.label_flag_pyro3_fired,     self.label_flag_pyro4_fired,
            self.label_flag_apogee_detected, self.label_flag_main_deployed,
            self.label_flag_drogue_deployed, self.label_flag_mach_lock_enabled,
        ]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            layout.addWidget(label)
        groupe.setLayout(layout)
        return groupe


    def _set_flag(self, label, actif):
        label.setStyleSheet("color: #4CAF50" if actif else "color: #F44336")


    def update_dico(self, dico):
        self.label_mission_state.setText(dico["mission_state"])
        self.label_battery.setText(f"{dico['battery_mv']:.5g} V")
        self.label_temp.setText(f"{dico['temp_celsius']:.5g} °C")
        self.label_pressure.setText(f"{dico['pressure_pa']:.5g} kPa")

        self.label_lat.setText(f"{dico['lat']} °")
        self.label_lon.setText(f"{dico['lon']} °")
        self.label_gps_alt.setText(f"{dico['gps_alt']:.5g} m")
        self.label_vel.setText(f"{dico['vel']:.5g} m/s")
        self.label_cog.setText(f"{dico['cog']:.5g} °")
        self.label_satellites_nb.setText(str(dico["satellites_nb"]))
        fix = dico["gps_fix"]
        self.label_gps_fix.setText("Fix" if fix else "No fix")
        self.label_gps_fix.setStyleSheet("color: #4CAF50" if fix else "color: #F44336")

        self.label_kalman_z.setText(f"{dico['kalman_z']:.5g} m")
        self.label_kalman_v.setText(f"{dico['kalman_v']:.5g} m/s")

        self.label_roll.setText(f"{dico['roll']:.5g} °")
        self.label_pitch.setText(f"{dico['pitch']:.5g} °")
        self.label_yaw.setText(f"{dico['yaw']:.5g} °")

        self.label_imu_acc_x.setText(f"{dico['imu_acc_x']:.5g} m/s²")
        self.label_imu_acc_y.setText(f"{dico['imu_acc_y']:.5g} m/s²")
        self.label_imu_acc_z.setText(f"{dico['imu_acc_z']:.5g} m/s²")
        self.label_imu_acc_vertical.setText(f"{dico['imu_acc_vertical']:.5g} m/s²")
        self.label_imu_gyro_x.setText(f"{dico['imu_gyro_x']:.5g} °/s")
        self.label_imu_gyro_y.setText(f"{dico['imu_gyro_y']:.5g} °/s")
        self.label_imu_gyro_z.setText(f"{dico['imu_gyro_z']:.5g} °/s")
        self.label_imu_mag_x.setText(f"{dico['imu_mag_x']:.5g} µT")
        self.label_imu_mag_y.setText(f"{dico['imu_mag_y']:.5g} µT")
        self.label_imu_mag_z.setText(f"{dico['imu_mag_z']:.5g} µT")

        self.label_highg_acc_x.setText(f"{dico['highg_acc_x']:.5g} m/s²")
        self.label_highg_acc_y.setText(f"{dico['highg_acc_y']:.5g} m/s²")
        self.label_highg_acc_z.setText(f"{dico['highg_acc_z']:.5g} m/s²")
        self.label_highg_acc_vertical.setText(f"{dico['highg_acc_vertical']:.5g} m/s²")

        self._set_flag(self.label_flag_idefix_ok,      dico["FLAG_IDEFIX_OK"])
        self._set_flag(self.label_flag_bt_ok,          dico["FLAG_BT_OK"])
        self._set_flag(self.label_flag_flash_ok,       dico["FLAG_FLASH_OK"])
        self._set_flag(self.label_flag_sd_ok,          dico["FLAG_SD_OK"])
        self._set_flag(self.label_flag_temp_ok,        dico["FLAG_TEMP_OK"])
        self._set_flag(self.label_flag_highg_ok,       dico["FLAG_HIGHG_OK"])
        self._set_flag(self.label_flag_gps_ok,         dico["FLAG_GPS_OK"])
        self._set_flag(self.label_flag_baro_ok,        dico["FLAG_BARO_OK"])
        self._set_flag(self.label_flag_imu_ok,         dico["FLAG_IMU_OK"])
        self._set_flag(self.label_flag_radio_ok,       dico["FLAG_RADIO_OK"])
        self._set_flag(self.label_flag_pyros_armed_ok, dico["FLAG_PYROS_ARMED_OK"])
        self._set_flag(self.label_flag_pyro1_conn,     dico["FLAG_PYRO1_CONN"])
        self._set_flag(self.label_flag_pyro2_conn,     dico["FLAG_PYRO2_CONN"])
        self._set_flag(self.label_flag_pyro3_conn,     dico["FLAG_PYRO3_CONN"])
        self._set_flag(self.label_flag_pyro4_conn,     dico["FLAG_PYRO4_CONN"])

        self._set_flag(self.label_flag_pyros_armed,       dico["FLAG_PYROS_ARMED"])
        self._set_flag(self.label_flag_pyro1_fired,       dico["FLAG_PYRO1_FIRED"])
        self._set_flag(self.label_flag_pyro2_fired,       dico["FLAG_PYRO2_FIRED"])
        self._set_flag(self.label_flag_pyro3_fired,       dico["FLAG_PYRO3_FIRED"])
        self._set_flag(self.label_flag_pyro4_fired,       dico["FLAG_PYRO4_FIRED"])
        self._set_flag(self.label_flag_apogee_detected,   dico["FLAG_APOGEE_DETECTED"])
        self._set_flag(self.label_flag_main_deployed,     dico["FLAG_MAIN_DEPLOYED"])
        self._set_flag(self.label_flag_drogue_deployed,   dico["FLAG_DROGUE_DEPLOYED"])
        self._set_flag(self.label_flag_mach_lock_enabled, dico["FLAG_MACH_LOCK_ENABLED"])

    def update_freq(self, freq_msg):
        self.label_freq_msg.setText(f"{freq_msg} Hz")



MISSION_COLORS = {
    "STATE_INIT":        "#888888",
    "STATE_PREFLIGHT":   "#2196F3",
    "STATE_ARMED":       "#FF9800",
    "STATE_INFLIGHT":    "#4CAF50",
    "STATE_POSTFLIGHT":  "#9C27B0",
    "STATE_UNKNOWN":     "#F44336",
}
 
 
def _load_obj(path):
    """Parse un fichier .obj → (vertices, faces) numpy."""
    vertices, faces = [], []
    with open(path) as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.split()[1:4])))
            elif line.startswith('f '):
                idx = [int(x.split('/')[0]) - 1 for x in line.split()[1:]]
                if len(idx) == 3:
                    faces.append(idx)
                elif len(idx) == 4:
                    faces.append([idx[0], idx[1], idx[2]])
                    faces.append([idx[0], idx[2], idx[3]])
    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.int32)


class TrajectoryMap(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.setMinimumSize(100, 100)
        # Cache des bornes
        self._lat_min = self._lat_max = None
        self._lon_min = self._lon_max = None

    def add_point(self, lat, lon):
        if lat == 0.0 and lon == 0.0:
            return
        self.points.append((lat, lon))
        # Mise à jour incrémentale des bornes
        if self._lat_min is None:
            self._lat_min = self._lat_max = lat
            self._lon_min = self._lon_max = lon
        else:
            self._lat_min = min(self._lat_min, lat)
            self._lat_max = max(self._lat_max, lat)
            self._lon_min = min(self._lon_min, lon)
            self._lon_max = max(self._lon_max, lon)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        painter.fillRect(0, 0, w, h, QColor(25, 25, 40))
        painter.setPen(QPen(QColor(70, 70, 90), 1))
        painter.drawRect(0, 0, w - 1, h - 1)

        if not self.points:
            painter.setPen(QPen(QColor(120, 120, 140)))
            painter.setFont(QFont("Arial", 9))
            painter.drawText(0, 0, w, h, Qt.AlignmentFlag.AlignCenter, "En attente GPS...")
            return

        lat_range = max(self._lat_max - self._lat_min, 0.0005)
        lon_range = max(self._lon_max - self._lon_min, 0.0005)
        pad = 20

        def to_screen(lat, lon):
            x = int((lon - self._lon_min) / lon_range * (w - 2 * pad) + pad)
            y = int((1 - (lat - self._lat_min) / lat_range) * (h - 2 * pad) + pad)
            return x, y

        # Ne dessiner que les 300 derniers points max
        points_visibles = self.points[-300:]
        if len(points_visibles) > 1:
            painter.setPen(QPen(QColor(100, 180, 255), 2))
            for i in range(1, len(points_visibles)):
                x1, y1 = to_screen(*points_visibles[i - 1])
                x2, y2 = to_screen(*points_visibles[i])
                painter.drawLine(x1, y1, x2, y2)

        x, y = to_screen(*self.points[-1])
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 60, 60))
        painter.drawEllipse(x - 6, y - 6, 12, 12)

        lat, lon = self.points[-1]
        painter.setPen(QPen(QColor(200, 200, 200)))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(5, 5, w - 10, 20, Qt.AlignmentFlag.AlignRight, f"{lat:.6f}, {lon:.6f}")
 
class RocketView3D(QWidget):
    def __init__(self, obj_path=None):
        super().__init__()
        self._gl_available = False
        self.mesh = None
        self._setup(obj_path)
 
    def _setup(self, obj_path):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
 
        try:
            import pyqtgraph.opengl as gl
 
            self.view = gl.GLViewWidget()
            self.view.setBackgroundColor('#1a1a2e')
            self.view.setCameraPosition(distance=5)
 
            axis = gl.GLAxisItem()
            axis.setSize(2, 2, 2)
            self.view.addItem(axis)
 
            if obj_path and os.path.exists(obj_path):
                verts, faces = _load_obj(obj_path)
                center = verts.mean(axis=0)
                verts -= center
                scale = 2.0 / np.abs(verts).max()
                verts *= scale
 
                md = gl.MeshData(vertexes=verts, faces=faces)
                self.mesh = gl.GLMeshItem(
                    meshdata=md,
                    smooth=True,
                    color=(0.8, 0.8, 0.9, 1.0),
                    shader='shaded',
                    glOptions='opaque'
                )
                self.view.addItem(self.mesh)
 
            self._gl_available = True
            layout.addWidget(self.view)
 
        except Exception as e:
            lbl = QLabel(f"3D non disponible\n{e}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #888;")
            layout.addWidget(lbl)
 
        self.setLayout(layout)
 
    def update_orientation(self, roll, pitch, yaw):
        if not self._gl_available or self.mesh is None:
            return
        self.mesh.resetTransform()
        self.mesh.rotate(yaw,   0, 0, 1)
        self.mesh.rotate(pitch, 0, 1, 0)
        self.mesh.rotate(roll,  1, 0, 0)
 
class PageBelle(QWidget):
    def __init__(self, obj_path=None):
        super().__init__()
 
        self._time_data = []
        self._alt_data  = []
        self._vel_data  = []
        self._acc_data  = []

        self.label_mission = QLabel("--")
        self.label_mission.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_mission.setFont(QFont("Arial", 16, QFont.Weight.Bold))
 
        self.label_time = QLabel("00:00.000")
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_time.setFont(QFont("Arial", 13))
        self.label_time.setStyleSheet("color: #AAAAAA;")

        self.rocket_view = RocketView3D(obj_path)

        self.map_view = TrajectoryMap()

        self.graph_alt = pg.PlotWidget(title="Altitude Kalman (m)")
        self.graph_alt.showGrid(x=True, y=True, alpha=0.3)
        self.graph_alt.setLabel('left', 'Altitude', units='m')
        self.graph_alt.setLabel('bottom', 'Temps', units='ms')
        self.curve_alt = self.graph_alt.plot(
            pen=pg.mkPen('#2196F3', width=2), name='Altitude'
        )

        self.graph_vel_acc = pg.PlotWidget(title="Vitesse & Accélération")
        self.graph_vel_acc.showGrid(x=True, y=True, alpha=0.3)
        self.graph_vel_acc.setLabel('bottom', 'Temps', units='ms')
        legend = self.graph_vel_acc.addLegend()
        self.curve_vel = self.graph_vel_acc.plot(
            pen=pg.mkPen('#4CAF50', width=2), name='Vitesse (m/s)'
        )

        self.graph_vel_acc.setLabel('left', 'Vitesse', units='m/s')
        self.curve_acc = self.graph_vel_acc.plot(
            pen=pg.mkPen('#FF9800', width=2), name='Acc. (m/s²)'
        )
 
        layout_principal = QHBoxLayout()
        layout_principal.setSpacing(6)
        layout_principal.setContentsMargins(6, 12, 6, 12)
 
        col_gauche = QVBoxLayout()
        col_gauche.setSpacing(4)
 
        row_mission = QHBoxLayout()
        row_mission.addWidget(self.label_mission, stretch=2)
        row_mission.addWidget(self.label_time,    stretch=1)
        col_gauche.addLayout(row_mission)
        col_gauche.addWidget(self.rocket_view, stretch=1)
        col_gauche.addWidget(self.map_view,    stretch=1)
 
        col_droite = QVBoxLayout()
        col_droite.setSpacing(4)
        col_droite.addWidget(self.graph_alt,     stretch=1)
        col_droite.addWidget(self.graph_vel_acc, stretch=1)
 
        layout_principal.addLayout(col_gauche, stretch=2)
        layout_principal.addLayout(col_droite, stretch=3)
 
        self.setLayout(layout_principal)

 
    def update_dico(self, dico):
        t   = dico["time_boot_ms"]
        alt = dico["kalman_z"]
        vel = dico["kalman_v"]
        acc = float(np.sqrt(
            dico["imu_acc_x"]**2 +
            dico["imu_acc_y"]**2 +
            dico["imu_acc_z"]**2
        ))
 
        self._time_data.append(t)
        self._alt_data.append(alt)
        self._vel_data.append(vel)
        self._acc_data.append(acc)

        self._time_data = self._time_data[-MAX_GRAPH_POINTS:]
        self._alt_data  = self._alt_data[-MAX_GRAPH_POINTS:]
        self._vel_data  = self._vel_data[-MAX_GRAPH_POINTS:]
        self._acc_data  = self._acc_data[-MAX_GRAPH_POINTS:]

        t_arr = np.array(self._time_data)
        self.curve_alt.setData(t_arr, np.array(self._alt_data))
        self.curve_vel.setData(t_arr, np.array(self._vel_data))
        self.curve_acc.setData(t_arr, np.array(self._acc_data))
 
        self.map_view.add_point(dico["lat"], dico["lon"])
        self.rocket_view.update_orientation(dico["roll"], dico["pitch"], dico["yaw"])
 
        mission = dico["mission_state"]
        color = MISSION_COLORS.get(mission, "#888888")
        self.label_mission.setText(mission)
        self.label_mission.setStyleSheet(
            f"color: {color}; font-size: 16px; font-weight: bold;"
        )
 
        ms     = int(t)
        mins   = ms // 60000
        secs   = (ms % 60000) // 1000
        millis = ms % 1000
        self.label_time.setText(f"{mins:02d}:{secs:02d}.{millis:03d}")

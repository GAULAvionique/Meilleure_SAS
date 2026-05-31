from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import sys


class PageFusee(QWidget):
    def __init__(self):
        super().__init__()

        # --- État général ---
        self.label_mission_state  = QLabel("mission_state: --")
        self.label_battery        = QLabel("battery: -- V")
        self.label_freq_msg       = QLabel("Fréquence messages: -- Hz")

        # --- GPS ---
        self.label_lat            = QLabel("lat: -- °")
        self.label_lon            = QLabel("lon: -- °")
        self.label_gps_alt        = QLabel("gps_alt: -- m")
        self.label_vel            = QLabel("vel: -- m/s")
        self.label_gps_fix        = QLabel("gps_fix: --")
        self.label_satellites_nb  = QLabel("satellites: --")
        self.label_cog            = QLabel("cog: -- °")

        # --- Kalman ---
        self.label_kalman_z       = QLabel("kalman_z: -- m")
        self.label_kalman_v       = QLabel("kalman_v: -- m/s")

        # --- Orientation ---
        self.label_roll           = QLabel("roll: -- °")
        self.label_pitch          = QLabel("pitch: -- °")
        self.label_yaw            = QLabel("yaw: -- °")

        # --- IMU ---
        self.label_imu_acc_x      = QLabel("imu_acc_x: -- m/s²")
        self.label_imu_acc_y      = QLabel("imu_acc_y: -- m/s²")
        self.label_imu_acc_z      = QLabel("imu_acc_z: -- m/s²")
        self.label_imu_gyro_x     = QLabel("imu_gyro_x: -- °/s")
        self.label_imu_gyro_y     = QLabel("imu_gyro_y: -- °/s")
        self.label_imu_gyro_z     = QLabel("imu_gyro_z: -- °/s")
        self.label_imu_mag_x      = QLabel("imu_mag_x: -- µT")
        self.label_imu_mag_y      = QLabel("imu_mag_y: -- µT")
        self.label_imu_mag_z      = QLabel("imu_mag_z: -- µT")
        self.label_imu_acc_vertical = QLabel("imu_acc_vertical: -- m/s²")

        # --- High-G ---
        self.label_highg_acc_x    = QLabel("highg_acc_x: -- m/s²")
        self.label_highg_acc_y    = QLabel("highg_acc_y: -- m/s²")
        self.label_highg_acc_z    = QLabel("highg_acc_z: -- m/s²")
        self.label_highg_acc_vertical = QLabel("highg_acc_vertical: -- m/s²")

        # --- Environnement ---
        self.label_pressure       = QLabel("pressure: -- hPa")
        self.label_temp           = QLabel("temp: -- °C")

        # --- Pyros ---
        #self.label_pyros_connected = QLabel("pyros_connected: --")

        # --- Layout temporaire (tout empilé verticalement) ---
        layout = QVBoxLayout()
        for attr in vars(self).values():
            if isinstance(attr, QLabel):
                layout.addWidget(attr)
        self.setLayout(layout)


    def update_dico(self, dico):
        self.label_mission_state.setText(f"mission_state: {dico['mission_state']}")
        self.label_battery.setText(f"battery: {dico['battery_mv']} V")

        self.label_lat.setText(f"lat: {dico['lat']} °")
        self.label_lon.setText(f"lon: {dico['lon']} °")
        self.label_gps_alt.setText(f"gps_alt: {dico['gps_alt']} m")
        self.label_vel.setText(f"vel: {dico['vel']} m/s")
        self.label_gps_fix.setText(f"gps_fix: {'Fix' if dico['gps_fix'] else 'No fix'}")
        self.label_satellites_nb.setText(f"satellites: {dico['satellites_nb']}")
        self.label_cog.setText(f"cog: {dico['cog']} °")

        self.label_kalman_z.setText(f"kalman_z: {dico['kalman_z']} m")
        self.label_kalman_v.setText(f"kalman_v: {dico['kalman_v']} m/s")

        self.label_roll.setText(f"roll: {dico['roll']} °")
        self.label_pitch.setText(f"pitch: {dico['pitch']} °")
        self.label_yaw.setText(f"yaw: {dico['yaw']} °")

        self.label_imu_acc_x.setText(f"imu_acc_x: {dico['imu_acc_x']} m/s²")
        self.label_imu_acc_y.setText(f"imu_acc_y: {dico['imu_acc_y']} m/s²")
        self.label_imu_acc_z.setText(f"imu_acc_z: {dico['imu_acc_z']} m/s²")
        self.label_imu_gyro_x.setText(f"imu_gyro_x: {dico['imu_gyro_x']} °/s")
        self.label_imu_gyro_y.setText(f"imu_gyro_y: {dico['imu_gyro_y']} °/s")
        self.label_imu_gyro_z.setText(f"imu_gyro_z: {dico['imu_gyro_z']} °/s")
        self.label_imu_mag_x.setText(f"imu_mag_x: {dico['imu_mag_x']} µT")
        self.label_imu_mag_y.setText(f"imu_mag_y: {dico['imu_mag_y']} µT")
        self.label_imu_mag_z.setText(f"imu_mag_z: {dico['imu_mag_z']} µT")
        self.label_imu_acc_vertical.setText(f"imu_acc_vertical: {dico['imu_acc_vertical']} m/s²")

        self.label_highg_acc_x.setText(f"highg_acc_x: {dico['highg_acc_x']} m/s²")
        self.label_highg_acc_y.setText(f"highg_acc_y: {dico['highg_acc_y']} m/s²")
        self.label_highg_acc_z.setText(f"highg_acc_z: {dico['highg_acc_z']} m/s²")
        self.label_highg_acc_vertical.setText(f"highg_acc_vertical: {dico['highg_acc_vertical']} m/s²")

        self.label_pressure.setText(f"pressure: {dico['pressure_hpa']} hPa")
        self.label_temp.setText(f"temp: {dico['temp_celsius']} °C")

        #self.label_pyros_connected.setText(f"pyros_connected: {dico['pyros_connected']}")


    def update_freq(self, freq_msg):
        self.label_freq_msg.setText(f"freq_msg: {freq_msg} Hz")



""" app = QApplication(sys.argv)
fenetre = QWidget()


layout_principal = QVBoxLayout()
layout_gps = QHBoxLayout()
layout_orientation = QHBoxLayout()
layout_system = QHBoxLayout()
layout_imu = QHBoxLayout()


layout_principal.addLayout(layout_gps)
layout_principal.addLayout(layout_orientation)
layout_principal.addLayout(layout_system)
layout_principal.addLayout(layout_imu)

layout_gps.addWidget(QLabel("latitude"))
layout_gps.addWidget(QLabel(str(d.dico_top["lat"])))
layout_gps.addWidget(QLabel("longitude"))
layout_gps.addWidget(QLabel(str(d.dico_top["lon"])))
layout_gps.addWidget(QLabel("altitude"))
layout_gps.addWidget(QLabel(str(d.dico_top["alt"])))
layout_gps.addWidget(QLabel("vitesse au sol"))
layout_gps.addWidget(QLabel(str(d.dico_top["vel"])))


fenetre.setLayout(layout_principal)
fenetre.setWindowTitle("Ground Station")
fenetre.show()
sys.exit(app.exec()) """
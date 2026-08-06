# --- Configuration du receiver ---

SERIAL_PORT = "/dev/tty.usbserial-BG00HQY4"
SERIAL_PORT = "udpin:0.0.0.0:14550"     # Décommenter pour tester virtuellement
BAUD_RATE = 115200
SOURCE_SYSTEM = 1
BOOSTER_SYS_ID = 2
SUSTAINER_SYS_ID = 3

RECV_TIMEOUT_S = 2.0
RECONNECT_DELAY_S = 2.0


# --- Configuration de mainWindow ---

ALT_MAX = 35000
ACC_MIN = -60
ACC_MAX = 120
VEL_MAX = 1200
VEL_MIN = -250

GRAPHS_REFRESH_RATE = 2000
MAX_GRAPH_POINTS = 5000


# --- Configuration de DataManager ---

CONVERSIONS = {                 # Dictionnaire de conversion : chaque valeur sera divisée par le nombre assicié 
                                # (attention que les clés soient exactement les mêmes que celle du dictionnaire décodé).
    "time_boot_ms"      : 1,
    "system_states"     : 1,
    "event_states"      : 1,
    "mission_state"     : 1,
    "battery_mv"        : 1000, # On a gardé le mv pour standardiser le nom des varibales, mais elle sera en V.

    "roll"              : 100,
    "pitch"             : 100,
    "yaw"               : 100,
    "imu_acc_x"         : 100,
    "imu_acc_y"         : 100,
    "imu_acc_z"         : 100,
    "imu_gyro_x"        : 100,
    "imu_gyro_y"        : 100,
    "imu_gyro_z"        : 100,
    "imu_mag_x"         : 100,
    "imu_mag_y"         : 100,
    "imu_mag_z"         : 100,

    "pressure_pa"       : 1000, # On a gardé le pa pour standardiser le nom des varibales, mais elle sera en kPa.
    "temp_celsius"      : 100,

    "highg_acc_x"       : 100,
    "highg_acc_y"       : 100,
    "highg_acc_z"       : 100,

    "gps_fix"           : 1,
    "lat"               : 1e7,
    "lon"               : 1e7,
    "gps_alt"           : 1000,
    "vel"               : 100,
    "cog"               : 100,
    "satellites_nb"     : 1,


    # "pyros_connected"   : 1,
    "imu_acc_vertical"  : 100,
    "highg_acc_vertical": 100,
    "kalman_z"          : 100,
    "kalman_v"          : 100,
    "altitude_msl_cm"   : 100,
}


SYSTEM_STATES_FLAGS = {         # Dictionnaire pour extraire les flags dans "system_states"
    "FLAG_IDEFIX_OK"      : 14,
    "FLAG_BT_OK"          : 13,
    "FLAG_FLASH_OK"       : 12,
    "FLAG_SD_OK"          : 11,
    "FLAG_TEMP_OK"        : 10,
    "FLAG_HIGHG_OK"       : 9,
    "FLAG_GPS_OK"         : 8,
    "FLAG_BARO_OK"        : 7,
    "FLAG_IMU_OK"         : 6,
    "FLAG_RADIO_OK"       : 5,
    "FLAG_PYROS_ARMED_OK" : 4,
    "FLAG_PYRO1_CONN"     : 3,
    "FLAG_PYRO2_CONN"     : 2,
    "FLAG_PYRO3_CONN"     : 1,
    "FLAG_PYRO4_CONN"     : 0,
}


EVENT_STATES_FLAGS = {          # Dictionnaire pour extraire les flags dans "event_states"
    "FLAG_PYROS_ARMED"       : 0,
    "FLAG_PYRO1_FIRED"       : 1,
    "FLAG_PYRO2_FIRED"       : 2,
    "FLAG_PYRO3_FIRED"       : 3,
    "FLAG_PYRO4_FIRED"       : 4,
    "FLAG_APOGEE_DETECTED"   : 5,
    "FLAG_MAIN_DEPLOYED"     : 6,
    "FLAG_DROGUE_DEPLOYED"   : 7,
    "FLAG_MACH_LOCK_ENABLED" : 8,
}


MISSION_STATES = {              # Dictionnaire pour donner du sens aux "mission_state"
    0: "STATE_INIT",
    1: "STATE_PREFLIGHT",
    2: "STATE_ARMED",
    3: "STATE_INFLIGHT",
    4: "STATE_POSTFLIGHT",
}


# --- Configuration pour la classe logger ---

CONTRAT = [         # Tout ce qui est dans cette liste sera dans le fichier log dans l'ordre. Le nom doit correspondre 
                    # à une valeur du dictionnaire de conversion.
    "time_boot_ms",
    "mission_state",
    "battery_mv",
    "roll",
    "pitch",
    "yaw",
    "imu_acc_x",
    "imu_acc_y",
    "imu_acc_z",
    "imu_gyro_x",
    "imu_gyro_y",
    "imu_gyro_z",
    "imu_mag_x",
    "imu_mag_y",
    "imu_mag_z",
    "pressure_pa",
    "temp_celsius",
    "highg_acc_x",
    "highg_acc_y",
    "highg_acc_z",
    "gps_fix",
    "lat",
    "lon",
    "gps_alt",
    "vel",
    "cog",
    "satellites_nb",
    # "pyros_connected",
    "imu_acc_vertical",
    "highg_acc_vertical",
    "kalman_z",
    "kalman_v",
    "altitude_msl_cm",

    "FLAG_IDEFIX_OK",
    "FLAG_BT_OK",
    "FLAG_FLASH_OK",
    "FLAG_SD_OK",
    "FLAG_TEMP_OK",
    "FLAG_HIGHG_OK",
    "FLAG_GPS_OK",
    "FLAG_BARO_OK",
    "FLAG_IMU_OK",
    "FLAG_RADIO_OK",
    "FLAG_PYROS_ARMED_OK",
    "FLAG_PYRO1_CONN",
    "FLAG_PYRO2_CONN",
    "FLAG_PYRO3_CONN",
    "FLAG_PYRO4_CONN",
    "FLAG_PYROS_ARMED",
    "FLAG_PYRO1_FIRED",
    "FLAG_PYRO2_FIRED",
    "FLAG_PYRO3_FIRED",
    "FLAG_PYRO4_FIRED",
    "FLAG_APOGEE_DETECTED",
    "FLAG_MAIN_DEPLOYED",
    "FLAG_DROGUE_DEPLOYED",
    "FLAG_MACH_LOCK_ENABLED",
]
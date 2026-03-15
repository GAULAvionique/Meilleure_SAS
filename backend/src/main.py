import data as data
import bitarray as bitarray
import numpy as np


if __name__ == "__main__":
    # Exemple d'utilisation
    raw_data = bytes.fromhex('244842FB000041B266660001E24042436F114012D8313DCCCCCDBD4CCCCD3CA3D70A0000000000000000411CF5C33FC00000C00000002AE1E10A')
    CONFIG_TRAME = {
        "start_char": (0, 8),          # Octet 0
        "header": (8, 8),              # Octet 1
        "altitude": (16, 32),          # Octet 2
        "temp": (48, 32),              # Octet 6
        "time_raw": (80, 32),          # Octet 10 (Non utilisé mais présent)
        "latitude": (112, 32),         # Octet 14
        "longitude": (144, 32),        # Octet 18
        "gyro_x": (176, 32),           # Octet 22
        "gyro_y": (208, 32),           # Octet 26
        "gyro_z": (240, 32),           # Octet 30
        "acc_x": (272, 32),            # Octet 34
        "acc_y": (304, 32),            # Octet 38
        "acc_z": (336, 32),            # Octet 42
        "kalman_roll": (368, 32),      # Octet 46
        "kalman_pitch": (400, 32),     # Octet 50
        "end_char_star": (432, 8),     # Octet 54
        "crc": (440, 16),              # Octet 55
        "line_feed": (456, 8)          # Octet 57
    }

#  Idée: créer une fonction d'initialisation à partir d'un fichier pour les deux config.
    CONFIG_TYPE = {
        "start_char": str,             # Char '$'
        "header": str,                # Char ou Byte
        "altitude": np.float32,        # 32-bit float
        "temp": np.float32,            # 32-bit float
        "time_raw": np.int32,          # 32-bit int (Non utilisé)
        "latitude": np.float32,        # 32-bit float
        "longitude": np.float32,       # 32-bit float
        "gyro_x": np.float32,          # 32-bit float
        "gyro_y": np.float32,          # 32-bit float
        "gyro_z": np.float32,          # 32-bit float
        "acc_x": np.float32,           # 32-bit float
        "acc_y": np.float32,           # 32-bit float
        "acc_z": np.float32,           # 32-bit float
        "kalman_roll": np.float32,     # 32-bit float
        "kalman_pitch": np.float32,    # 32-bit float
        "end_char_star": str,          # Char '*'
        "crc": np.uint16,              # 16-bit unsigned int
        "line_feed": str               # Char '\n'
    }

    RÉSULTAT = {
        "start_char": (0, 8),          # Octet 0
        "header": (8, 8),              # Octet 1
        "altitude": (16, 32),          # Octet 2
        "temp": (48, 32),              # Octet 6
        "time_raw": (80, 32),          # Octet 10 (Non utilisé mais présent)
        "latitude": (112, 32),         # Octet 14
        "longitude": (144, 32),        # Octet 18
        "gyro_x": (176, 32),           # Octet 22
        "gyro_y": (208, 32),           # Octet 26
        "gyro_z": (240, 32),           # Octet 30
        "acc_x": (272, 32),            # Octet 34
        "acc_y": (304, 32),            # Octet 38
        "acc_z": (336, 32),            # Octet 42
        "kalman_roll": (368, 32),      # Octet 46
        "kalman_pitch": (400, 32),     # Octet 50
        "end_char_star": (432, 8),     # Octet 54
        "crc": (440, 16),              # Octet 55
        "line_feed": (456, 8)          # Octet 57
    }

    trame = data.data(raw_data, CONFIG_TRAME, CONFIG_TYPE, RÉSULTAT)
    print(trame.raw)
    trame.décode()
    print(trame.trameDécodé)
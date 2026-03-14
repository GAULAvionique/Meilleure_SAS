import data as data
import bitarray as bitarray
import numpy as np


if __name__ == "__main__":
    # Exemple d'utilisation
    raw_data = bytes.fromhex('24 54 42 34 00 00 00 2D 00 00 54 54 46 20 14 00 24')
    CONFIG_TRAME = {
        "start_bit": (0, 8),
        "vid": (8, 4),
        "seq": (12, 3),
        "hb": (15, 1),
        "data_moteur": (16, 32),
        "data_test": (32, 32),
        "e1": (80, 4),
        "e2": (84, 12),
        "timestamp": (96, 32),
        "ending_bit": (128, 8)
    }

#  Idée: créer une fonction d'initialisation à partir d'un fichier pour les deux config.
    CONFIG_TYPE = {
        "start_bit": str,
        "vid": bitarray,
        "seq": bitarray,
        "hb": bool,
        "data_moteur": np.float32,
        "data_test": np.int32,
        "e1": bitarray,
        "e2": bitarray,
        "timestamp": np.float32,
        "ending_bit": str
    }

    RÉSULTAT = {
        "start_bit": str,
        "vid": bitarray,
        "seq": bitarray,
        "hb": bool,
        "data_moteur": np.float32,
        "data_test": np.int32,
        "e1": int,
        "e2": float,
        "timestamp": float,
        "ending_bit": str
    }

    trame = data.data(raw_data, CONFIG_TRAME, CONFIG_TYPE, RÉSULTAT)
    print(trame.raw)
    trame.décode()
    print(trame.trameDécodé)
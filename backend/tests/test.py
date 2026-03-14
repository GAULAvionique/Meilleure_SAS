from bitarray import bitarray
import numpy as np

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

#Idée: créer une fonction d'initialisation à partir d'un fichier pour les deux config.
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
    "data_test": np.int,
    "e1": int,
    "e2": float,
    "timestamp": float,
    "ending_bit": str
}


binary_str = "01100001"

# 1. Conversion de la base 2 vers l'entier
decimal_value = int(binary_str, 2) 
print(decimal_value)

# 2. Conversion de l'entier vers le caractère (ASCII/Unicode)
character = chr(decimal_value)

print(f"Binaire: {binary_str} -> Entier: {decimal_value} -> Texte: {character}")
# Sortie : Binaire: 01100001 -> Entier: 97 -> Texte: a
from bitarray import bitarray
import numpy as np

CONFIG_TRAME = {
    "start_bit": (0, 8),
    "vid": (8, 4),
    "seq": (12, 3),
    "hb": (15, 1),
    "data_moteur": (16, 64),
    "e1": (80, 4),
    "e2": (84, 12),
    "timestamp": (96, 16),
    "crc16": (112, 16),
    "ending_bit": (128, 8)
}


binary_str = "01100001"

# 1. Conversion de la base 2 vers l'entier
decimal_value = int(binary_str, 2) 
print(decimal_value)

# 2. Conversion de l'entier vers le caractère (ASCII/Unicode)
character = chr(decimal_value)

print(f"Binaire: {binary_str} -> Entier: {decimal_value} -> Texte: {character}")
# Sortie : Binaire: 01100001 -> Entier: 97 -> Texte: a
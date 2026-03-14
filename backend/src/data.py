from bitarray import bitarray
import numpy as np


# Dictionnaire de configuration pour l'extraction des données du message
# Le premier chiffre représente la position de départ
# Le second chiffre représente la longueur en bits
CONFIG_TRAME = {
    "start_bit": (0, 8),
    "vid": (8, 4),
    "seq": (12, 3),
    "hb": (15, 1),
    "data_moteur": (16, 32),
    "data_test": (32, 32),
    "e1": (80, 4),
    "e2": (84, 12),
    "timestamp": (96, 16),
    "crc16": (112, 16),
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
    "e2": float,
    "timestamp": float,
    "crc16": float,
    "ending_bit": str
}

RÉSULTAT = {
    "start_bit": str,
    "vid": bitarray,
    "seq": bitarray,
    "hb": bool,
    "data_moteur": np.float32,
    "e1": int,
    "e2": float,
    "timestamp": float,
    "crc16": float,
    "ending_bit": str
}


class data:
    def __init__(self, raw_data, configTrame, configType, trameDécodé):
        self.raw = int.from_bytes(raw_data, byteorder='big')
        self.config = configTrame
        self.longueurTotale = len(raw_data) * 8
        self.configType = configType
        self.trameDécodé = trameDécodé


    def __séquencer(self, config_key):
        # Extraction de la séquence à partir du message en bits
        start_bit, length = self.config[config_key]
        décalage = self.longueurTotale - (start_bit + length)
        masque = (1 << length) - 1
        return (self.raw >> décalage) & masque
    

    def __convertir(self, message, type, longueur):

        # La méthode supporte actuellement string, float32, int32, bitarray et bool
        if type == str:
            return 

        if type == np.float32:
            return float(np.array([message], dtype=np.uint32).view(np.float32)[0])
        
        if type == np.int32:
            return int(message)
        
        if type == bitarray: # bitarray a été utilisé au cas où le message n'est pas 8 bits
            return bitarray(format(message, str(longueur) + 'b'))
        
        if type == bool:
            return bool(message)
        

    def décode(self):
        for morceau in self.config:
            #chaine = bitarray(uint=self.__séquenceur(morceau), self.config[morceau][1])
            intMessage = self.__séquencer(morceau)
            self.trameDécodé[morceau] = self.__convertir(intMessage, self.configType[morceau], self.config[morceau][1])


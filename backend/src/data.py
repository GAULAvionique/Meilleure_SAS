# Dictionnaire de configuration pour l'extraction des données du message
# Le premier chiffre représente la position de départ du champ
# Le second chiffre représente la longueur du champ en bits
Peut-être rajouter le type pour code plus maléable
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


class data:
    def __init__(self, raw_data, config):
        self.raw = int.from_bytes(raw_data, byteorder='big')
        self.config = config
        self.longueurTotale = len(raw_data) * 8

    def séquenceur(self, config_key):
        # Extraction de la séquence à partir du message en bits
        start_bit, length = self.config[config_key]
        décalage = self.longueurTotale - (start_bit + length)
        masque = (1 << length) - 1
        return (self.raw >> décalage) & masque
        
    def décode(self):
        informations = self.config
        for trame in self.config:
            informations[trame] = self.config[trame]

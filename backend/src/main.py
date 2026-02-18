import data as data


if __name__ == "__main__":
    # Exemple de données brutes (17 octets)
    raw_data = bytes.fromhex('01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF 02')
    
    # Création d'une instance de la classe data avec les données brutes et la configuration
    message = data.data(raw_data, data.CONFIG_TRAME)
    
    # Extraction des différentes séquences à partir du message
    start_bit = message.séquenceur("start_bit")
    vid = message.séquenceur("vid")
    seq = message.séquenceur("seq")
    hb = message.séquenceur("hb")
    data_moteur = message.séquenceur("data_moteur")
    e1 = message.séquenceur("e1")
    e2 = message.séquenceur("e2")
    timestamp = message.séquenceur("timestamp")
    crc16 = message.séquenceur("crc16")
    ending_bit = message.séquenceur("ending_bit")
    
    # Affichage des résultats
    print(f"Start Bit: {start_bit}")
    print(f"VID: {vid}")
    print(f"Sequence: {seq}")
    print(f"HB: {hb}")
    print(f"Data Moteur: {data_moteur}")
    print(f"E1: {e1}")
    print(f"E2: {e2}")
    print(f"Timestamp: {timestamp}")
    print(f"CRC16: {crc16}")
    print(f"Ending Bit: {ending_bit}")
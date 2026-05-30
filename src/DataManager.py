from config import CONVERSIONS, SYSTEM_STATES_FLAGS, EVENT_STATES_FLAGS, MISSION_STATES, BOOSTER_SYS_ID, SUSTAINER_SYS_ID
from PySide6.QtCore import QObject, Signal
import threading
import queue


class DataManager(QObject):
    signal_sustainer = Signal(dict)
    signal_booster = Signal(dict)

    def __init__(self, logger_top, logger_bot, data_queue):
        super().__init__()

        self.queue = data_queue             # Queue remplie par le receiver
        self.logger_top = logger_top        # Objet logger de MyLogger correspondant au haut de la fusée
        self.logger_bot = logger_bot        # Objet logger de MyLogger correspondant au bas de la fusée

        self.dico_top = {}                  # Dictionnaire de l'état présent pour le haut de la fusée
        self.dico_bot = {}                  # Dictionnaire de l'état présent pour le bas de la fusée

        self._running = threading.Event()
        self._running.set()

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()


    def _scaling(self, dico):
        for key in dico:
            if key in CONVERSIONS:
                if CONVERSIONS[key] != 1:
                    dico[key] /= CONVERSIONS[key]
            else:
                if key != "mavpackettype":
                    print(f"La clé {key} n'est pas définie dans 'CONVERSIONS'.")
        

    def _extract_flags(self, dico):

        system_states = {}
        event_states = {}
        for key in SYSTEM_STATES_FLAGS:
            system_states[key] = bool(dico["system_states"] & (1 << SYSTEM_STATES_FLAGS[key]))

        for key in EVENT_STATES_FLAGS:
            event_states[key] = bool(dico["event_states"] & (1 << EVENT_STATES_FLAGS[key]))
        
        del dico["system_states"]
        del dico["event_states"]

        dico.update(system_states)
        dico.update(event_states)


    def _extract_enum(self, dico):
        try:
            dico["mission_state"] = MISSION_STATES[dico["mission_state"]]
        except KeyError:
            dico["mission_state"] = "STATE_UNKNOWN"


    def _read(self, msg):
        dico = msg.to_dict()
        self._scaling(dico)
        self._extract_flags(dico)
        self._extract_enum(dico)

        if msg.get_srcSystem() == SUSTAINER_SYS_ID:
            self.dico_top = dico
            self.logger_top.log(dico)
            self.signal_sustainer.emit(dico)
            
        elif msg.get_srcSystem() == BOOSTER_SYS_ID:
            self.dico_bot = dico
            self.logger_bot.log(dico)
            self.signal_booster.emit(dico)


        else:
            print("Le message provient d'une source inconnue")


    def _run(self):
        while self._running.is_set():
            try:
                ligne = self.queue.get(timeout=0.1)
                self._read(ligne)
            except queue.Empty:
                continue

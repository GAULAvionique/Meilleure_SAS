import queue
import threading
import csv
from config import CONTRAT


class MyLogger:
    def __init__(self, nomFichier):     # Contrat est la liste de tout ce qu'on veut afficher dans le fichier ex. ['time', 'altitude', 'speedX'].
        self.fichier = open(nomFichier, 'w')
        self.writer = csv.DictWriter(self.fichier, fieldnames=CONTRAT, extrasaction='ignore', restval='N/A') # Se fie à CONTRAT,
        # si une données est de trop, il l'ignore et si une données est manquante, il écrit N/A
        self.writer.writeheader()

        self.queue = queue.Queue()

        self._working = threading.Event()
        self._working.set()

        self.thread = threading.Thread(target=self._worker)
        self.thread.start()

    
    def _worker(self):                          # Le worker est appelé automatiquement lorsque l'objet est créé.
        while self._working.is_set():
            try:
                données = self.queue.get(timeout=0.1)
                self.writer.writerow(données)
                self.fichier.flush()
            except queue.Empty:
                continue


    def log(self, données):                     # Méthode pour ajouter un paquet de données dans la queue du worker.
        self.queue.put(données)


    def stop(self):                             # Cette méthode doit être appelé pour terminer correctement l'exécution du thread.
        self._working.clear()
        self.thread.join()

        while not self.queue.empty():
            try:
                données = self.queue.get_nowait()
                self.writer.writerow(données)
            except queue.Empty:
                break
                
        self.fichier.flush()
        self.fichier.close()

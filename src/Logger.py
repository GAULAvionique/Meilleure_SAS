import queue
import threading
from config import CONTRAT


class MyLogger:
    def __init__(self, nomFichier):     # Contrat est la liste de tout ce qu'on veut afficher dans le fichier ex. ['time', 'altitude', 'speedX'].
        self.fichier = open(nomFichier, 'w')

        header = ",".join(CONTRAT)
        self.fichier.write(header + '\n')

        self.queue = queue.Queue()

        self._working = threading.Event()
        self._working.set()

        self.thread = threading.Thread(target=self._worker)
        self.thread.start()

    
    def _worker(self):                          # Le worker est appelé automatiquement lorsque l'objet est créé.
        while self._working.is_set():
            try:
                ligne = self.queue.get(timeout=0.1)
                self.fichier.write(ligne)
                self.fichier.flush()
            except queue.Empty:
                continue


    def log(self, données):                     # Méthode pour ajouter un paquet de données dans la queue du worker.
        affichage = ''
        for item in CONTRAT:
            affichage += str(données[item]) + ','

        affichage = affichage[:-1] + '\n'
        self.queue.put(affichage)


    def stop(self):                             # Cette méthode doit être appelé pour terminer correctement l'exécution du thread.
        self._working.clear()
        self.thread.join()
        self.fichier.close()

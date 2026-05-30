## Station au sol

Le code de la station au sol se divise en plusieurs modules qui se complètent mutuellement. Le backend a été conçu pour être facilement modifiable, mais le frontend devra probablement être modifié à chaque année. 

# Code de la station au sol

Le receiver met le message mavlink dans un objet queue que DataManager convertit en dictionnaire de données standardisées. DataManager s'occupe ensuite de distribuer le contenu à l'interface et à la classe MyLogger. Voici une description plus détaillée de ce qu'accomplit chaque module:

- Receiver : Effectue la connexion entre la radio RFD900X branchée à la station au sol et le logiciel avec PyMAVLink. La fonction prend en entrée: serial_port, source_system, baud_rate et data_queue. Cette fonction prend le message reçu et le met dans un objet queue. Elle Elle doit rouler dans un thread qui existe dans le main. Important: Il faut s'assurer que le fichier odb_mavlink_v1.py, qui a été copié depuis le code de l'ODB, soit à jour.

- DataManager : Classe qui s'occupe de toute la gestion de données des deux parties de la fusée séparément. Il prend les messages MAVLink de la queue, convertit les unités (centidegrés -> degrés, millivolts -> volts, etc.), extrait les flags et traduit mission_state en string lisible. Ensuite les envoie au bon logger et à l'interface grâce à un signal QT. En entrée, on a les deux logger (un pour le booster et un pour le sustainer) et la queue du receiver. Les constantes dans config.py doivent être à jour. Lorsque l'instance est créée, un thread est lancé à l'intérieur de la classe, dans lequel la méthode _run() s'exécute. 

- MyLogger : Classe très générale qui écrit ce qu'on lui donne en entrée de sa méthode log(), dans un fichier. La fonction log() prend en entrée un dictionnaire et écrit uniquement les valeurs dont les clés sont présentes dans CONTRAT (config.py), en ignorant le reste. La classe prend en paramètre le nom d'un fichier et crée celui-ci en y ajoutant des données à chaque fois que log() est appelé. Les fichiers se retrouveront dans le dossier logs. Lorsque l'instance est créée, un thread est lancé à l'intérieur de la classe, dans lequel la méthode _worker() s'exécute.

- MainWindow : Code de l'interface (codé à la main) qui reçoit un signal QT et affiche le contenu du signal (dictionnaire) dans l'interface.

Le fichier config.py contient la configuration du receiver, du DataManager et du Logger.

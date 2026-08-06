from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
from pathlib import Path

app = QApplication([])

print("Répertoire courant :", Path.cwd())

logo = Path("logo_gaul.png")
print("Existe :", logo.exists())
print("Chemin absolu :", logo.resolve())

pixmap = QPixmap(str(logo))
print("Pixmap valide :", not pixmap.isNull())

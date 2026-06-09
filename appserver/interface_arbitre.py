import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QTextEdit,
    QTableWidget,
    QPushButton,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime

class SignauxServeur(QObject):
    nouveau_score = pyqtSignal(str, int, str,str)
class FenetreArbitre(QMainWindow):
    def __init__(self):
        super().__init__()
        self.radio = SignauxServeur()
        self.radio.nouveau_score.connect(self.mise_a_jour_tableau)

        self.setWindowTitle("Interface arbitre")
        self.setGeometry(100, 100, 800, 600)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal_horizontal = QHBoxLayout()
        colonne_gauche_verticale = QVBoxLayout()
        colonne_droite_verticale = QVBoxLayout()

        # à enlever plus tard
        simulation_button = QPushButton("simulation")
        simulation_button.clicked.connect(self.simuler_reception)

        self.list_robot = QListWidget()
        boite_robots = QGroupBox("Robots en piste")
        layout_interne_robot = QVBoxLayout()
        layout_interne_robot.addWidget(self.list_robot)
        layout_interne_robot.addWidget(simulation_button)
        boite_robots.setLayout(layout_interne_robot)

        self.score = QTableWidget()
        boite_score = QGroupBox("Score")
        layout_interne_score = QVBoxLayout()
        layout_interne_score.addWidget(self.score)
        boite_score.setLayout(layout_interne_score)
        self.score.setColumnCount(2)
        self.score.setHorizontalHeaderLabels(["Nom du Robot", "Score Final"])
        self.score.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.score.verticalHeader().setVisible(False)
        self.score.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        boite_log = QGroupBox("Log")
        layout_interne_log = QVBoxLayout()
        layout_interne_log.addWidget(self.log)
        boite_log.setLayout(layout_interne_log)

        colonne_gauche_verticale.addWidget(boite_robots)
        colonne_droite_verticale.addWidget(boite_score)
        colonne_droite_verticale.addWidget(boite_log)

        layout_principal_horizontal.addLayout(colonne_gauche_verticale)
        layout_principal_horizontal.addLayout(colonne_droite_verticale)

        widget_central.setLayout(layout_principal_horizontal)
        self.regle = textToDictionnaire("appserver/exemple.battle")

    def mise_a_jour_tableau(self, nom_robot, score, mouvement, expression) :
        self.list_robot.addItem(nom_robot)
        self.log.append(f"{datetime.now().strftime('%H:%M:%S')} {nom_robot} a fait le mouvement {mouvement} avec l'expression {expression}")
        ligne_actuelle = self.score.rowCount()
        
        self.score.insertRow(ligne_actuelle)
        boite_score = QTableWidgetItem(str(score))
        boite_nom = QTableWidgetItem(nom_robot)
        boite_nom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        boite_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score.setItem(ligne_actuelle,1,boite_score)
        self.score.setItem(ligne_actuelle,0,boite_nom)

    def simuler_reception(self):
        self.radio.nouveau_score.emit("Robot_Test", 10, "ALU", "XNG")




def textToDictionnaire(fichier):
    regles = {}
    couleur_actuelle = None
    with open(fichier, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("MVS"):
                morceaux = line.split(" ")
                regles[morceaux[0]] = int(morceaux[1].strip())
            line = line.strip()
            if line.startswith("["):
                couleur_actuelle = line[1]
                regles[couleur_actuelle] = {}
            elif "=" in line:
                morceaux = line.split("=")
                regles[couleur_actuelle][morceaux[0]] = int(morceaux[1].strip())
    print(regles)
    return regles


def calculerScore(json, regle):
    col = json["col"]
    arm = json["arm"]
    exp = json["exp"]

    score = 0
    arm_propre = arm.replace(" ", "+")
    arm_propre = sorted(arm_propre.split("+"))
    exp_propre = exp.replace(" ", "+")
    if(not col in regle):
        return 0 #si la couleur n'est pas dans les regles alors on renvoie 0

    for key in regle[col]:
        key_propre = sorted(key.split("+"))

        if arm_propre == key_propre or exp_propre == key:
            score += regle[col][key]

        elif "," in key:
            key_propre = key.split(",")
            for action in key_propre:
                if action in arm_propre:
                    score += regle[col][key]
                    break
                if action in exp_propre:
                    score += regle[col][key]
                    break

    return score


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fenetre = FenetreArbitre()
    fenetre.show()

    sys.exit(app.exec())

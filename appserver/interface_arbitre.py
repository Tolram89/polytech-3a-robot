import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit, QTableWidget, QLabel, QPushButton
from PyQt6.QtWidgets import QGroupBox 
class FenetreArbitre(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Interface arbitre")
        self.setGeometry(100, 100, 800, 600) 
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal_horizontal = QHBoxLayout()
        colonne_gauche_verticale = QVBoxLayout()
        colonne_droite_verticale = QVBoxLayout()
        
        #à enlever plus tard
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
        
    def simuler_reception(self) :
        self.list_robot.addItem("Robot ABC123")
        self.log.append("[10:42] Robot ABC123 a fait le mouvement ALU")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    fenetre = FenetreArbitre()
    fenetre.show()
    
    sys.exit(app.exec())


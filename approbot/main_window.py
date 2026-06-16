import time
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QGroupBox, QTabWidget
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import http_client

class ConnexionWorker(QThread):
    succes = pyqtSignal(object)
    erreur = pyqtSignal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        try:
            from martypy import Marty
            self.succes.emit(Marty("wifi", self.ip))
        except Exception as e:
            self.erreur.emit(str(e))

class BatterieWorker(QThread):
    resultat = pyqtSignal(int)
    erreur   = pyqtSignal(str)

    def __init__(self, marty):
        super().__init__()
        self.marty = marty

    def run(self):
        try:
            self.resultat.emit(int(self.marty.get_battery_remaining()))
        except Exception as e:
            self.erreur.emit(str(e))

class ActionWorker(QThread):
    fini  = pyqtSignal()
    erreur = pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        try:
            self.fn()
            self.fini.emit()
        except Exception as e:
            self.erreur.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.marty = None
        self.setWindowTitle("AppoRobot")
        self.setMinimumSize(520, 480)
        self._build_ui()

        self.timer_batterie = QTimer(self)
        self.timer_batterie.setInterval(5000)
        self.timer_batterie.timeout.connect(self._lire_batterie)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(self._panneau_connexion())
        layout.addWidget(self._panneau_batterie())

        self.onglets = QTabWidget()
        self.onglets.addTab(self._onglet_principal(), "Principal")
        self.onglets.addTab(self._onglet_manuel(), "Manuel")
        layout.addWidget(self.onglets, stretch=1)

    def _panneau_connexion(self):
        grp = QGroupBox("Connexion")
        row = QHBoxLayout(grp)
        
        row.addWidget(QLabel("IP Robot :"))
        self.champ_ip = QLineEdit("192.168.0.101")
        row.addWidget(self.champ_ip)
    
        row.addWidget(QLabel("IP Serveur :"))
        self.champ_ip_serveur = QLineEdit("192.168.0.100")
        row.addWidget(self.champ_ip_serveur)
        
        self.btn_connect = QPushButton("Connecter")
        self.btn_connect.clicked.connect(self._connecter)
        row.addWidget(self.btn_connect)
        
        self.btn_disconnect = QPushButton("Déconnecter")
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.clicked.connect(self._deconnecter)
        row.addWidget(self.btn_disconnect)
        
        return grp

    def _panneau_batterie(self):
        grp = QGroupBox("Batterie")
        row = QHBoxLayout(grp)
        self.label_batterie = QLabel("–")
        row.addWidget(self.label_batterie)
        row.addStretch()
        return grp

    def _onglet_principal(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        
        self.btn_charger_dance = QPushButton("Charger et Lancer une Chorégraphie (.dance)")
        self.btn_charger_dance.setMinimumHeight(40) 
        self.btn_charger_dance.clicked.connect(self._charger_choregraphie)
        layout.addWidget(self.btn_charger_dance)

        self.journal = QTextEdit()
        self.journal.setReadOnly(True)
        layout.addWidget(self.journal)
        return w
    
    def _charger_choregraphie(self):
        if not self.marty:
            self.log("Erreur : Veuillez vous connecter au robot d'abord.")
            return

        from PyQt6.QtWidgets import QFileDialog
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner la chorégraphie",
            "",
            "Fichiers Dance (*.dance);;Tous les fichiers (*)"
        )

        if chemin_fichier:
            self.log(f"Fichier chargé : {chemin_fichier}")
            self.log("Démarrage de la battle...")
            
            self._action(
                lambda: __import__('choregraphie').executer_choregraphie(self.marty, chemin_fichier),
                "Battle", 
                "Chorégraphie terminée avec succès !"
            )

    def _onglet_manuel(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)

        layout.addWidget(self._groupe_deplacements())
        layout.addWidget(self._groupe_bras())
        layout.addWidget(self._groupe_expressions())

        btn_neutre = QPushButton("Position neutre (bras + expression)")
        btn_neutre.clicked.connect(self._position_neutre)
        layout.addWidget(btn_neutre)

        layout.addStretch()
        return w

    def _groupe_deplacements(self):
        grp = QGroupBox("Déplacements (1 pas)")
        grid = QVBoxLayout(grp)

        row1 = QHBoxLayout()
        row1.addStretch()
        btn_avant = QPushButton("↑ Avancer")
        btn_avant.clicked.connect(lambda: self._action(
            lambda: __import__('deplacement').avancer(self.marty), "Déplacement", "Avancer"))
        row1.addWidget(btn_avant)
        row1.addStretch()
        grid.addLayout(row1)

        row2 = QHBoxLayout()
        btn_gauche = QPushButton("← Gauche")
        btn_gauche.clicked.connect(lambda: self._action(
            lambda: __import__('deplacement').gauche(self.marty), "Déplacement", "Gauche"))
        row2.addWidget(btn_gauche)

        btn_reculer = QPushButton("↓ Reculer")
        btn_reculer.clicked.connect(lambda: self._action(
            lambda: __import__('deplacement').reculer(self.marty), "Déplacement", "Reculer"))
        row2.addWidget(btn_reculer)

        btn_droite = QPushButton("→ Droite")
        btn_droite.clicked.connect(lambda: self._action(
            lambda: __import__('deplacement').droite(self.marty), "Déplacement", "Droite"))
        row2.addWidget(btn_droite)

        grid.addLayout(row2)
        return grp

    def _groupe_bras(self):
        grp = QGroupBox("Bras")
        row = QHBoxLayout(grp)

        for label, commande in [
            ("Bras G levé",     "ALU"),
            ("Bras G arrière",  "ALB"),
            ("Bras D levé",     "ARU"),
            ("Bras D arrière",  "ARB"),
        ]:
            btn = QPushButton(label)
            cmd = commande
            btn.clicked.connect(lambda _, c=cmd: self._action(
                lambda c=c: __import__('bras').appliquer_bras(self.marty, [c]),
                "Bras", c))
            row.addWidget(btn)

        return grp

    def _groupe_expressions(self):
        grp = QGroupBox("Expressions")
        row = QHBoxLayout(grp)

        for label, commande in [
            ("Neutre",  "XNT"),
            ("Triste",  "XSD"),
            ("Énervé",  "XNG"),
            ("Content", "XHP"),
            ("Enjoué",  "XDN"),
        ]:
            btn = QPushButton(label)
            cmd = commande
            btn.clicked.connect(lambda _, c=cmd: self._action(
                lambda c=c: __import__('expression').appliquer_expression(self.marty, c),
                "Expression", c))
            row.addWidget(btn)

        return grp

    def _connecter(self):
        ip = self.champ_ip.text().strip()
        if not ip:
            return
        self.btn_connect.setEnabled(False)
        self.btn_connect.setText("Connexion…")
        self._worker = ConnexionWorker(ip)
        self._worker.succes.connect(self._on_ok)
        self._worker.erreur.connect(self._on_erreur)
        self._worker.start()

    def _on_ok(self, marty):
        self.marty = marty
        self.btn_connect.setText("Connecter")
        self.btn_disconnect.setEnabled(True)
        self.log(f"Connecté à {self.champ_ip.text().strip()}")
        self._lire_batterie()
        self.timer_batterie.start()

        ip_serveur = self.champ_ip_serveur.text().strip()
        if ip_serveur:
            http_client.HOST = ip_serveur
            
        http_client.hello()

    def _on_erreur(self, msg):
        self.btn_connect.setEnabled(True)
        self.btn_connect.setText("Connecter")
        self.log(f"Erreur connexion : {msg}")

    def _deconnecter(self):
        if self.marty:
            try:
                self.marty.close()
            except Exception:
                pass
            self.marty = None
        self.timer_batterie.stop()
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.label_batterie.setText("–")
        self.log("Déconnecté")
        http_client.bye()

    def _lire_batterie(self):
        if not self.marty:
            return
        self._bat_worker = BatterieWorker(self.marty)
        self._bat_worker.resultat.connect(lambda n: self.label_batterie.setText(f"{n}%"))
        self._bat_worker.erreur.connect(lambda e: self.log(f"Batterie erreur : {e}"))
        self._bat_worker.start()

    def _action(self, fn, type_action: str, detail: str):
        if not self.marty:
            self.log("Non connecté")
            return
        w = ActionWorker(fn)
        w.fini.connect(lambda: self.log(f"{type_action} : {detail}"))
        w.erreur.connect(lambda e: self.log(f"Erreur {type_action} : {e}"))
        w.start()
        self._action_worker = w

    def _position_neutre(self):
        if not self.marty:
            self.log("Non connecté")
            return
        def fn():
            __import__('bras').position_neutre(self.marty)
            __import__('expression').appliquer_expression(self.marty, 'XNT')
        self._action(fn, "Position", "Neutre")

    def log(self, message: str):
        heure = time.strftime("%H:%M:%S")
        self.journal.append(f"[{heure}] {message}")

    def get_marty(self):
        return self.marty
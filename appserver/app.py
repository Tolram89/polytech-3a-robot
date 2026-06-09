from interface_arbitre import FenetreArbitre
from http_serveur import demarrer_serveur
import threading
import sys
import signal # 1. L'import pour gérer le Ctrl+C
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)#pour que le controle C fonctionne

    app = QApplication(sys.argv)
    fenetre = FenetreArbitre()

    mon_thread = threading.Thread(target=demarrer_serveur, args=(fenetre.radio,))
    
    mon_thread.daemon = True #le serveur se ferme quand on fait ctrl C

    mon_thread.start()
    fenetre.show()
    sys.exit(app.exec())
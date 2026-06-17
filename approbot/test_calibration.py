# test_calibration.py
# Script de calibrage : affiche les 4 canaux du capteur de couleur toutes les 5 secondes.
# Pose le robot sur une couleur, lis les valeurs, puis reporte-les dans VALEURS_REFERENCE.

import time

from conn import connection
from detection_couleur import lire_canaux


def main():
    ip = input("Entrer l'ip du Marty : ").strip()
    if not ip:
        ip = "192.168.0.104"
        print("ip par defaut :", ip)

    marty = connection(ip)
    if marty is None:
        print("Connexion echouée")
        return

    print("\nLecture du capteur toutes les 5 secondes. (Ctrl+C pour arrêter)\n")

    try:
        while True:
            clear, red, green, blue = lire_canaux(marty)
            print(f"clear={clear}  red={red}  green={green}  blue={blue}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nArrêt du calibrage.")
    finally:
        marty.close()
        print("deconnexion")


if __name__ == '__main__':
    main()

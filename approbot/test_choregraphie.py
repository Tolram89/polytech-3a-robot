from marty_mock import MartyMock
from choregraphie import executer_choregraphie

def test_choregraphie():
    marty = MartyMock()
    marty.valeur_capteur_simulee = 150
    try:
        executer_choregraphie(marty, r"C:\Users\coren\Documents\Polytech-DIJON\Année 2025-2026\Projet_Robotique\polytech-3a-robot\approbot\choregraphie.dance")
    except Exception as e:
        print(f"Erreur : {e}")
    print("Historique des actions :")
    for action in marty.historique:
        print(action)

test_choregraphie()
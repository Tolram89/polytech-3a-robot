def textToDictionnaire(fichier) :
    regles = {}
    couleur_actuelle = None
    with open(fichier, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("MVS"):
                morceaux = line.split(" ")
                regles[morceaux[0]] = morceaux[1].strip()
            line = line.strip()
            if line.startswith("["):
                couleur_actuelle = line[1]
                regles[couleur_actuelle]={}
    print(regles)
            
                


textToDictionnaire("appserver/exemple.battle")
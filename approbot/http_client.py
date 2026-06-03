import http.client
import json

HOST = 'localhost'
PORT = 1632

rid = -1  # rid 


def _send_and_read(method, path, body=None):
    conn = http.client.HTTPConnection(HOST, PORT)
    conn.request(method, path, body=body)
    reponse = conn.getresponse()
    return reponse.read().decode('utf-8')


def hello():
    #demande un rid au serveur, premiere chose a faire
    global rid
    try:
        rid = _send_and_read('POST', '/hello')
        print("RID reçu -> " + rid)
    except Exception as e:
        print("Erreur send_hello : " + str(e))


def start():
    # Déclare le démarrage d'une chorégraphie, renvoie le nombre de pas décidé par le serveur
    if rid == -1:
        print("faire le hello()")
        return None
    json_message = json.dumps({"rid": rid})
    try:
        nbr_pas = _send_and_read('POST', '/start', body=json_message)
        print("Nombre de pas : " + nbr_pas)
        return int(nbr_pas)
    except Exception as e:
        print("Erreur start : " + str(e))
        return None


def step(col, arm, exp):
    # Envoie un pas au serveur (couleur, mouvement de bras, expression), renvoie les points obtenus
    if rid == -1:
        print("faire le hello()")
        return None
    json_message = json.dumps({"rid": rid, "col": col, "arm": arm, "exp": exp})
    try:
        points = _send_and_read('POST', '/step', body=json_message)
        print(f"Points obtenus : {points}")
        return int(points)
    except Exception as e:
        print("Erreur step : " + str(e))
        return None


def bye():
    # Déconnecte le robot du serveur
    if rid == -1:
        return
    json_message = json.dumps({"rid": rid})
    try:
        reponse = _send_and_read('POST', '/bye', body=json_message)
        print("Déconnexion : " + reponse)
    except Exception as e:
        print("Erreur bye : " + str(e))




if __name__ == '__main__':
    hello()
    #start(10)
    step("G", "ALU+ARU","XNT")

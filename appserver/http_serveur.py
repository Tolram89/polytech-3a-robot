from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import random, string
import json
from interface_arbitre import calculerScore, textToDictionnaire


version = "1"
robot_list = {}  # dico des robots connectés {ip: rid}
scores = {}      # score de chaque robot {rid: points}
compteur_pas = {} # nombre de pas chaque robot {rid : nombre de pas}
REGLES_BATTLE= textToDictionnaire("appserver/exemple.battle")

class Server(BaseHTTPRequestHandler):


    def do_GET(self):
        #teste requete 
        parsed = urlparse(self.path)

        if parsed.path == '/':
            # retourne version serv
            self.ok_response(version)

        elif parsed.path == '/score':
            #test si pas corrompue
            params = parse_qs(parsed.query)
            if 'rid' not in params:
                self.send_error(400, "rid manquant")
                return

            rid = params['rid'][0]

            # test que le robot est bien enregistrer
            if rid not in robot_list.values():
                self.send_error(403, "robot inconnu")
                return

            # retourne le score du robot 
            score = scores.get(rid, 0)
            print(f"Score pour {rid} : {score}")
            self.ok_response(str(score))

        else:
            self.send_error(404, "requete inconnue")

    def do_POST(self):
        # gestion requetes post
        if self.path == '/hello':
            self.hello_response()
        elif self.path == '/start':
            self.start_response()
        elif self.path == '/step':
            self.step_response()
        elif self.path == '/bye':
            self.bye_response()
        else:
            self.send_error(404, "route inconnue")

    def read_json_body(self):
        #lis la requete json
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400, "requete vide")
            return None
        try:
            return json.loads(self.rfile.read(content_length).decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "JSON invalide")
            return None

    def check_rid(self, data):
        # Vérifie que le champ rid est présent et que le robot est enregistré
        if 'rid' not in data:
            self.send_error(400, "Champ rid manquant")
            return None
        rid = data['rid']
        if rid not in robot_list.values():
            self.send_error(403, "Robot inconnu, faire /hello avant")
            return None
        return rid

    def start_response(self):
        # debut choré
        data = self.read_json_body()
        if data is None:
            return
        rid = self.check_rid(data)
        if rid is None:
            return
        
        compteur_pas[rid] = 0

        nbr_mouvement_chore = REGLES_BATTLE['MVS']

        print(f"debur choré  {rid} : {nbr_mouvement_chore} pas")
        self.ok_response(str(nbr_mouvement_chore))

    def step_response(self):
        # get les mvt du robot
        data = self.read_json_body()
        if data is None:
            return
        rid = self.check_rid(data)
        if rid is None:
            return
        if rid not in compteur_pas:
            self.send_error(400, "le robot doit faire start")
            return
        for field in ('col', 'arm', 'exp'):
            if field not in data:
                self.send_error(400, f"Champ {field} manquant")
                return
        col = data['col']
        arm = data['arm']
        exp = data['exp']
        if compteur_pas[rid] < REGLES_BATTLE['MVS'] :
            compteur_pas[rid]+=1
            points = calculerScore(data, REGLES_BATTLE)
            scores[rid] = scores.get(rid, 0) + points
            self.radio.nouveau_score.emit(rid, scores[rid] , arm, exp, points)
            self.ok_response(str(points))
        else :
            self.send_error(403, "Chorégraphie terminée, nombre de pas max atteint")
            return

    def bye_response(self):
        # deco le robot et le retire de la liste des robots connus
        data = self.read_json_body()
        if data is None:
            return
        rid = self.check_rid(data)
        if rid is None:
            return
        ip = next(ip for ip, r in robot_list.items() if r == rid)
        del robot_list[ip]
        self.radio.nouvel_evenement.emit(f"Déconnexion du robot {rid}")
        self.ok_response("deconnexion reussie")

    def ok_response(self, message="OK"):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def generate_rid(self):
        #permet de generer un RID unique sous la forme AAA123

        while True:
            rid = ''.join(random.choices(string.ascii_uppercase, k=3)) + \
                  ''.join(random.choices(string.digits, k=3))
            # Recommence si le RID est déjà utilisé
            if rid not in robot_list.values():
                return rid

    def hello_response(self):
        #enregistre le robot et renvoi son RID
        ip = self.client_address[0]

        #reutilise le RID existant si ip connue
        if ip not in robot_list:
            robot_list[ip] = self.generate_rid()
        self.radio.nouvel_evenement.emit(f"Connexion de {ip} -> RID : {robot_list[ip]}")
        self.ok_response(robot_list[ip])
        self.radio.nouveau_robot.emit(robot_list[ip])



def demarrer_serveur(radio_recue):
    Server.radio = radio_recue 
    
    PORT = 1632
    serveur = HTTPServer(('', PORT), Server)
    print(f"Serveur démarré sur le port {PORT}")
    serveur.serve_forever()






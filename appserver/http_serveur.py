from http.server import HTTPServer, BaseHTTPRequestHandler
import random, string
import json


version = "1"
robot_list = {}

class Server(BaseHTTPRequestHandler):

    def do_POST(self):

        #SI hello() -> return ID
        #SI start(id)-> nbr de pas a faire
        #SI step(id, couleur relevé, mvt de bras, expression realisée)-> score
        #SI bye(id)-> deconnexion robot
        
        self.process_response()
        
            
        #self.do_GET()


    

    def process_response(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')

        data = json.loads(message)


        if(data['content'] == "\n"):
            print("ID envoyer")
            self.nothing_response()

        elif(data['content'] == "hello"):
            self.hello_response()


        #si pas message de debut, on test que le robot a bien mit son ID
        elif(data['rid'] in robot_list.values()): 
            if(data['content'] == "start"):
                #on demare une chorer de nbr_pas 
                nbr_pas = data['nb'] 
                print("Debut de chorée de "+ str(nbr_pas)+" pas.")
                self.do_GET()
                print("start")

            else:
                print(data['content'])
                self.do_GET()

        else:
            pass

    def do_GET(self):

        self.send_response(200)  # Code 200 = OK
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        reponse = "Message bien reçu !"
        self.wfile.write(reponse.encode('utf-8'))



    def nothing_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(version.encode('utf-8'))


    def start_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(version.encode('utf-8'))

    def generate_rid(self):
        while True:
            rid = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=3))
            if rid not in robot_list:
                return rid
            

    def new_client(self):
        #test si l'ip est deja connu
        ip = self.client_address[0]
        if ip not in robot_list:
            robot_list[ip] = self.generate_rid()

    def hello_response(self):
        ip = self.client_address[0]
        self.new_client()
        print("ajout de "+ ip +" -> " + robot_list[ip])

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
                         
        response = json.dumps({"rid": robot_list[ip]}) + "\n"
        self.wfile.write(response.encode('utf-8'))



# Créer et démarrer le serveur
PORT = 1632
serveur = HTTPServer(('', PORT), Server)
print(f"Serveur démarré sur le port {PORT}")
serveur.serve_forever()
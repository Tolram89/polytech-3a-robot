import socket
from concurrent.futures import ThreadPoolExecutor
import psutil
from functools import partial



#recup l'ip local de la machine
def get_mon_ip():
    interfaces = psutil.net_if_addrs()

    for nom_interface in interfaces:
        adresses = interfaces[nom_interface]
        for adr in adresses:

            #test si IPV4
            if adr.family == socket.AF_INET:
                ip = adr.address
                if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
                    return ip
  
    return None

#recup l prefixe (la partie reseau)
def get_prefixe(ip):
    if ip:
        parties = ip.split('.')
        prefixe = parties[0] + '.' + parties[1] + '.' + parties[2] + '.'
        return prefixe
    return None



#envoue une requete sur le port 80 pour tester si il est ouvert -> marty
def port_ouvert(ip, port=80, timeout=2.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    finally:
        s.close()



#fonction pour tester quon va mettre dans le thread
def tester(ip, port, timeout):
    if port_ouvert(ip, port, timeout):
        return ip
    else:
        return None





#Si return = None -> probleme lors du traitement
#Si return= [] liste vide -> pas de martys trouver 
#Sinon [ip1,ip2,..]. -> liste des Marty
def scan_reseau(port=80, timeout=2.0):
    
    #ip du reseau
    prefixe = get_prefixe(get_mon_ip())
    
    if prefixe:

        print("Debut du scann...")

        ips = []
        for n in range(2, 255):
            ips.append(prefixe + str(n))

        
        # thread pour tester toutes les ip en meme temps

        with ThreadPoolExecutor(max_workers=100) as executor:
            resultats = executor.map(partial(tester, port=port, timeout=timeout), ips)

        # on garde que les ip valides
        trouves = []
        for ip in resultats:
            if ip is not None:
                trouves.append(ip)

        return trouves
    else:
        return None
        



if __name__ == '__main__':

    resultats = scan_reseau()

    if resultats == None:
        print("Erreur dans le traitement de l'ip de la machine")
        
    elif len(resultats) >= 1: 
        print("IP des Martys : ", resultats)
    else:
        print("Aucun Marty trouvé")
    
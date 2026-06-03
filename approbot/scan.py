import socket
from concurrent.futures import ThreadPoolExecutor
import psutil


def get_mon_ip():
    interfaces = psutil.net_if_addrs()

    for nom_interface in interfaces:
        adresses = interfaces[nom_interface]
        for adr in adresses:
            if adr.family == socket.AF_INET:
                ip = adr.address
                if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
                    return ip
    return "127.0.0.1"


def get_prefixe(ip):
    #192.168.1.5 -> 192.168.1.
    parties = ip.split('.')
    prefixe = parties[0] + '.' + parties[1] + '.' + parties[2] + '.'
    return prefixe


def port_ouvert(ip, port=80, timeout=2.0):
    # Teste si le port est ouvert sur une IP donnée, true si ouvert false si fermer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout) 

    try:
        s.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    finally:
        s.close()  


def scan_reseau(port=80, timeout=2.0):
    prefixe = get_prefixe(get_mon_ip())  

    ips = []
    for n in range(2, 255):
        ips.append(prefixe + str(n))


    def tester(ip):
        if port_ouvert(ip, port, timeout):
            return ip
        else:
            return None

    #thread poour tester toute les ip en meme temps
    with ThreadPoolExecutor(max_workers=100) as executor:
        resultats = executor.map(tester, ips)

    # on garde que les ip valide
    trouves = []
    for ip in resultats:
        if ip is not None:
            trouves.append(ip)

    return trouves


if __name__ == '__main__':
    print("Scan en cours")
    resultats = scan_reseau()
    print(f"{len(resultats)} IP des Martys : {resultats}")
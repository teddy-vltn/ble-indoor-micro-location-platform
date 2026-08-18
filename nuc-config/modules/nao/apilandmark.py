# coding=utf-8
import requests
import time
from naoqi import ALProxy

# Configuration des proxies
NAO_IP = "192.168.1.11"
NAO_PORT = 9559

API_IP = "192.168.2.1"
API_PORT = "5001"

# Initialisation des proxies
memoryProxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
markProxy = ALProxy("ALLandMarkDetection", NAO_IP, NAO_PORT)
markProxy.subscribe("Test_Mark", 50, 0.0)
tabletProxy = ALProxy("ALTabletService", NAO_IP, NAO_PORT)

# API URLs
API_URL_FIND = "http://"+ API_IP + ":" + str(API_PORT) + "/players/search"
API_URL_NEW = "http://" + API_IP + ":" + str(API_PORT) + "/players"
API_URL_END = "http://" + API_IP + ":" + str(API_PORT) + "/players/{}/finish"
API_URL_HAS_VISITED = "http://" + API_IP + ":" + str(API_PORT) + "/players/{}/has-visited"  

DELAI_MINIMUM = 1
derniere_requete = {}

def show_dialog(message):
    tabletProxy.showInputDialog("text", message, "OK", "Annuler")
    print(message)

def verifier_session(id_naomark):
    response = requests.get(API_URL_FIND + "?id_minor=" + str(id_naomark))
    print("GET request to: {} with params: {}".format(API_URL_FIND, {"id_minor": id_naomark}))
    print(response)
    return response.json()

def joueur_detecte(id_naomark):
    temps_actuel = time.time()
    if id_naomark not in derniere_requete or (temps_actuel - derniere_requete[id_naomark] > DELAI_MINIMUM):
        derniere_requete[id_naomark] = temps_actuel

        r = verifier_session(id_naomark)

        if not r.get("data") or not r["data"]["players"]:
            data = {'id_minor': id_naomark, 'devices': ['pepper-1']}
            response = requests.post(API_URL_NEW, json=data)
            print("POST request to: {} with data: {}".format(API_URL_NEW, data))
            if response.status_code == 200:
                show_dialog("Bienvenue au musée, joueur {}. Votre session de jeu commence !".format(id_naomark))
        else:
            player_data = r["data"]["players"][0]
            player_id = player_data["_id"]
            secteurs_a_visiter = ['1', '2']  # Exemple de secteurs requis
            data = {'nodes': secteurs_a_visiter}
            response = requests.post(API_URL_HAS_VISITED.format(player_id), json=data).json()
            if response.get("data") and response["data"]["visited"]:
                show_dialog("Félicitations, vous avez visité tous les secteurs requis !")
                requests.put(API_URL_END.format(player_id))
            else:
                show_dialog("Il semble que vous n'ayez pas encore visité tous les secteurs. Continuez à explorer !")
    else:
        print("Requête trop récente, veuillez attendre.")

try:
    while True:
        val = memoryProxy.getData("LandmarkDetected")
        if val and len(val) > 1:
            print("Found")
            id_naomark = val[1][0][1][0]
            joueur_detecte(id_naomark)
except KeyboardInterrupt:
    print("Arrêt du script")
    markProxy.unsubscribe("Test_Mark")

import os
import sys
import datetime
import time
import csv
import lib.settings as settings

date = None
logs_dir_path = None
log_file_path = None
csv_file_path = None
csv_data_cache = None
logs = None


def checkIfDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Liste pour stocker les logs
def init():
    global date, logs_dir_path, log_file_path, csv_file_path, csv_data_cache, logs

    csv_data_cache = []
    logs = []
    date = time.strftime("%Y-%m-%d", time.localtime())

    logs_dir_path = settings.get("logs_dir_path")

    checkIfDirectoryExists(logs_dir_path)

    log_file_path = os.path.join(logs_dir_path, f"logs-{date}.txt")
    csv_dir_path = settings.get("csv_dir_path")

    checkIfDirectoryExists(csv_dir_path)

    csv_file_path = os.path.join(csv_dir_path, f"data-{date}.csv")


# Fonction pour écrire les logs dans un fichier
def write_logs_to_file():
    with open(log_file_path, "a") as file:
        for log in logs:
            file.write(f"{log}\n")
    logs.clear()


def write_csv_data_to_file():
    with open(csv_file_path, "a", newline="") as csvfile:
        fieldnames = ["identity", "datetime", "major", "minor", "tx_power", "rssi"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for data in csv_data_cache:
            writer.writerow(data)
    csv_data_cache.clear()


# Gestionnaire de signal pour gérer les signaux de fermeture
def signal_handler(signum, frame):
    print(f"Signal de fermeture {signum} reçu, écriture des logs dans le fichier...")

    # On rajoute une log pour indiquer que le script a été fermé
    log("Fermeture du script")

    write_logs_to_file()
    write_csv_data_to_file()
    sys.exit(0)


def log(message):

    dt = datetime.datetime.now().strftime("%F %T.%f")[:-3]
    id = settings.get("hostname")

    logs.append(id + " " + dt + " " + message)

    if logs.__len__() >= settings.get("log_cache_size"):
        write_logs_to_file()


def logcsv(data: dict):
    data["datetime"] = time.time()
    data["identity"] = settings.get("hostname")

    csv_data_cache.append(data)

    if len(csv_data_cache) >= settings.get("csv_cache_size"):
        write_csv_data_to_file()

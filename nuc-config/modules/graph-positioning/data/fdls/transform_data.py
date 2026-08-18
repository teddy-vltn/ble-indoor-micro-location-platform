import csv
import json
from pathlib import Path

def convert_date_format(date_str):
    # Transformer 2023-10-10 18:53:48.850 en 2023-10-10 18:53:48.000
    return date_str.split('.')[0] + '.000'

def process_csv_file(csv_file_path):
    transformed_data = []
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # Exemple de row: ['rasp25', '2023-10-10 18:53:48.850', '8888', '3', '-87', '-70']

            hostname = row[0].strip().strip('\x00')


            transformed_data.append({
                "rssi": int(row[5]),
                "major": int(row[2]),
                "date": str(row[1]),
                "hostname": hostname,
                "minor": int(row[3])
            })
    return transformed_data

# Supposons un chemin racine où les dossiers des Raspberries sont stockés
root_path = Path("data/fdls/FDLS2023-microloc")
all_data = []

for csv_file in root_path.rglob('data-14.csv'):
    all_data.extend(process_csv_file(csv_file))

# Sauvegarder all_data dans un fichier JSON
with open("data/fdls/beacons.json", "w") as jsonfile:
    json.dump(all_data, jsonfile)

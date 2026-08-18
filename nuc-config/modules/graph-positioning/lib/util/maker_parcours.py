import time
import sys
import json

def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convert_to_timestamp(date_str):
    # Convert date string to a timestamp
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")))

def generate_output(data):
    result = []
    capteur_id = 1
    for date_str, items in data.items():
        last_capteur = items["to"][-1]
        for capteur in items["to"]:
            synchronized = last_capteur == capteur
            result.append({
                "timestamp": convert_to_timestamp(date_str),
                "capteur": capteur,
                "synchronized": synchronized,
                "stop": synchronized
            })
        capteur_id += 1
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 maker_gml.py input.txt")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = input_file_path.rsplit('.', 1)[0] + ".json"

    data = read_data_from_json(input_file_path)
    result = generate_output(data)

    with open(output_file_path, 'w') as f:
        json.dump(result, f)

    
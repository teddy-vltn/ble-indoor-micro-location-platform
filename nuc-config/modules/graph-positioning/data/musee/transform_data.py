
## read json beacons_userId.json and transform it to map
import json
import datetime

input_json = {}

with open('beacons_userId.json') as f:
    input_json = json.load(f)

## transform data

output_json = []
for item in input_json:
    user_id = item['userId']
    beacons = item['beacons']
    beacons = json.loads(beacons)
    for beacon in beacons:
        beacon["date"] = beacon["timeStamp"]
        transformed_beacon = {
            "rssi": beacon["RSSI"] if "RSSI" in beacon else 0,
            "major": beacon["major"] if "major" in beacon else 0,
            # date to timestamp 20210919T09:13:51
            "timestamp": datetime.datetime.strptime(beacon["date"], "%Y%m%dT%H:%M:%S").timestamp(),
            "hostname": beacon["minor"] if "minor" in beacon else 0,
            "minor": user_id
        }
        output_json.append(transformed_beacon)
        
## write json beacons.json
with open('beacons.json', 'w') as f:
    json.dump(output_json, f)
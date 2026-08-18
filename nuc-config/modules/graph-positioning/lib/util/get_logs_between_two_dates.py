import json 
from pymongo import MongoClient

with open("./config.json", "r") as file:
    config = json.load(file)

MONGO_CONNECTION = config["MONGO_CONNECTION"]

client = MongoClient(MONGO_CONNECTION["URI"])
db = client[MONGO_CONNECTION["DATABASE"]]

logs = db[MONGO_CONNECTION["LOGS_COLLECTION"]]

def get_logs_between_two_dates(start_date, end_date):
    global logs
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lt": end_date
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "date": "$date",
                    "hostname": "$hostname",
                    "rssi": "$rssi",
                    "tx_power": "$tx_power",
                    "major": "$major",
                    "minor": "$minor"
                },
                "document": {"$first": "$$ROOT"}
            }
        },
        {
            "$replaceRoot": {"newRoot": "$document"}
        },
        {
            "$project": {
                "tx_power": 1,
                "rssi": 1,
                "minor": 1,
                "major": 1,
                "hostname": 1,
                "date": 1,
                "_id": 0
            }
        }
    ]
    results = logs.aggregate(pipeline, allowDiskUse=True)  # Enable disk use
    return list(results)

l = get_logs_between_two_dates("2024-05-01", "2024-05-03")

# write to file
with open("logs.json", "w") as file:
    json.dump(l, file)
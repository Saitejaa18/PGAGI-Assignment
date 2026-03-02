import json
from datetime import datetime

def save_candidate_data(data):
    filename = "candidates.json"
    try:
        with open(filename, "r") as file:
            existing = json.load(file)
    except:
        existing = []

    data["timestamp"] = datetime.utcnow().isoformat()
    existing.append(data)

    with open(filename, "w") as file:
        json.dump(existing, file, indent=4)

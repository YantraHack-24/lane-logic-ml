import json

data = {
    0: {
        "ambulance": 0,
        "bicycles": 1,
        "buses": 1,
        "trucks": 1,
        "vans": 0,
        "cars": 1,
        "trains": 1,
        "tractors": 0,
    },
    1: {
        "ambulance": 0,
        "bicycles": 1,
        "buses": 1,
        "trucks": 1,
        "vans": 0,
        "cars": 1,
        "trains": 1,
        "tractors": 0,
    },
    2: {
        "ambulance": 0,
        "bicycles": 1,
        "buses": 1,
        "trucks": 1,
        "vans": 0,
        "cars": 1,
        "trains": 1,
        "tractors": 0,
    },
    3: {
        "ambulance": 0,
        "bicycles": 1,
        "buses": 1,
        "trucks": 1,
        "vans": 0,
        "cars": 1,
        "trains": 1,
        "tractors": 0,
    },
}

# Replace single quotes with double quotes
json_data = json.dumps(
    {str(k): {str(k2): v2 for k2, v2 in v.items()} for k, v in data.items()}
)

print(json_data)

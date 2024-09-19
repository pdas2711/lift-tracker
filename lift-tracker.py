#!/usr/bin/env python

import json
from sys import argv

def get_movement_id(movements, movement):
    for index in movements:
        if movements[index]["name"] == movement:
            return index
    movement_entry = {
                "name": movement
            }
    movements[str(len(movements) + 1)] = movement_entry
    return str(len(movements) + 1)

def get_location_id(locations, location):
    for index in locations:
        if locations[index] == location:
            return index
    locations[str(len(locations) + 1)] = location
    return str(len(locations) + 1)

def import_csv(data_file, location, filename):
    with open(filename, "r") as f:
        csv_data = f.readlines()
    header_data = csv_data.pop(0)
    for record in csv_data:
        date = None
        for col_index, column in enumerate(header_data.split(",")):
            entry = {
                    "date": None,
                    "movement": None,
                    "average_metric": None,
                    "sets": "Not Available",
                    "location": get_location_id(data_file["locations"], location)
            }
            if col_index == 1:
                date = record.split(",")[col_index]
                continue
            else:
                entry["date"] = date
                entry["movement"] = get_movement_id(data_file["movements"], column)
                entry["average_metric"] = record.split(",")[col_index]
            data_file["data"].append(entry)

def generate_data_file(filename):
    data_file = {
            "movements": {},
            "locations": {},
            "data": []
            }
    with open(filename, "w") as f:
        f.write(json.dumps(data_file))

data_filename = "data.json"
if argv[1] == "new":
    generate_data_file(data_filename)
elif argv[1] == "import":
    set_location = False
    location = None
    for arg in argv:
        if set_location:
            location = arg
            set_location = False
        if arg == "--location":
            set_location = True
    if not location:
        location = input("Location: ")
    with open(data_filename, "r") as f:
        data_file = json.loads(f.read())
    import_csv(data_file, location, argv[-1])
    with open(data_filename, "w") as f:
        f.write(json.dumps(data_file))
else:
    print("Error: Unknown argument '" + argv[1] + "'")
    exit()

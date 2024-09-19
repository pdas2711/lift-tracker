#!/usr/bin/env python

import json
from sys import argv
from time import strptime

def add_movement_id(movements, movement, group):
    movement_entry = {
                "name": movement,
                "group": group
            }
    movements[str(len(movements) + 1)] = movement_entry
    return str(len(movements))

def add_location_id(locations, location):
    locations[str(len(locations) + 1)] = location
    return str(len(locations))

def get_movement_id(movements, movement):
    for index in movements:
        if movements[index]["name"] == movement:
            return index
    return None

def get_location_id(locations, location):
    for index in locations:
        if locations[index] == location:
            return index
    return None

def import_csv(data_file, location, group, filename):
    with open(filename, "r") as f:
        csv_data = f.read().splitlines()
    header_data = csv_data.pop(0)
    for record in csv_data:
        date = None
        for col_index, column in enumerate(header_data.split(",")):
            location_id = get_location_id(data_file["locations"], location)
            if not location_id:
                location_id = add_location_id(data_file["locations"], location)
            entry = {
                    "date": None,
                    "movement": None,
                    "average_metric": None,
                    "sets": "Not Available",
                    "location": location_id
            }
            if col_index == 0:
                date = record.split(",")[col_index]
                continue
            elif record.split(",")[col_index] == "":
                continue
            else:
                entry["date"] = date
                movement_id = get_movement_id(data_file["movements"], column)
                if not movement_id:
                    movement_id = add_movement_id(data_file["movements"], column, group)
                entry["movement"] = movement_id
                entry["average_metric"] = record.split(",")[col_index]
            data_file["data"].append(entry)

def sort(data):
    def quick_sort(sub_array, i, j, p):
        p = len(sub_array) - 1
        while j < p:
    quick_sort(data, i = -1, j = 0)

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
    set_group = False
    location = None
    group = None
    for arg in argv:
        if set_location:
            location = arg
            set_location = False
        if set_group:
            group = arg
            set_group = False
        if arg == "--location":
            set_location = True
        if arg == "--group":
            set_group = True
    if not location:
        location = input("Location: ")
    if not group:
        group = input("Group: ")
    with open(data_filename, "r") as f:
        data_file = json.loads(f.read())
    import_csv(data_file, location, group, argv[-1])
    with open(data_filename, "w") as f:
        f.write(json.dumps(data_file))
else:
    print("Error: Unknown argument '" + argv[1] + "'")
    exit()

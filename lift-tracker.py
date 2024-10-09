#!/usr/bin/env python

import json
from sys import argv
from datetime import datetime
from datetime import timezone

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
                date_fields = []
                for date_field in record.split(",")[col_index].split("/"):
                    date_fields.append(date_field)
                year = "20" + date_fields[2]
                month = date_fields[0]
                day = date_fields[1]
                date = year + "/" + month + "/" + day
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
            bubble_sort(data_file["data"])

def compare_dates(date1, date2):
    date1_form = datetime(int(date1.split("/")[0]), int(date1.split("/")[1]), int(date1.split("/")[2]))
    date2_form = datetime(int(date2.split("/")[0]), int(date2.split("/")[1]), int(date2.split("/")[2]))
    if date1_form > date2_form:
        return True
    else:
        return False

def bubble_sort(array):
    for i in range(len(array)):
        swapped = False
        for j in range(0, len(array) - i - 1):
            if compare_dates(array[j]["date"], array[j + 1]["date"]):
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
        if not swapped:
            break

def add_entry(data_file):
    print("\nChoose a movement.")
    for movement_index in data_file["movements"]:
        print(movement_index + ". " + data_file["movements"][movement_index]["name"])
    movement_opt = input("\nEnter Existing Movement or type New Movement: ")
    if movement_opt not in data_file["movements"]:
        print("\nAdding '" + movement_opt + "'.")
        group = input("Group: ")
        add_movement_id(data_file["movements"], movement_opt, group)
    print("\nLast metric.")
    last_date = "Not Available"
    last_avg_metric = "Not Available"
    for entry_index in range(len(data_file["data"]) - 1, -1, -1):
        last_entry = data_file["data"][entry_index]
        if last_entry["movement"] == movement_opt:
            last_date = last_entry["date"]
            last_avg_metric = last_entry["average_metric"]
    print("Date: " + last_date)
    print("Movement: " + data_file["movements"][movement_opt]["name"])
    print("Metric: " + last_avg_metric)
    print("\nChoose a location.")
    current_loc = None
    for location_index in data_file["locations"]:
        print(location_index + ". " + data_file["locations"][location_index])
    location_opt = input("Enter Existing Location or type New Location: ")
    if location_opt not in data_file["locations"]:
        print("\nAdding '" + location_opt + "'.")
        data_file["locations"][str(len(data_file) + 1)] = location_opt
        current_loc = location_opt
    else:
        current_loc = data_file["locations"][location_opt]
    print("\nEnter the rep and metric amount. When done, enter '0' to exit.")
    sets = []
    set_entry = {
            "time": None,
            "duration": None,
            "weight": None,
            "reps": None
            }
    set_opt = None
    entry_time = datetime.now(timezone.utc)
    while set_opt != "0":
        print("\n1. Add New Set")
        print("0. Done")
        set_opt = input("Option: ")
        if set_opt == "1":
            time = datetime.now(timezone.utc)
            print("Current Time: " + time.strftime("%H:%M:%S"))
            metric_weight = input("Weight: ")
            metric_rep = input("Reps: ")
            end_time = datetime.now(timezone.utc)
            set_entry["weight"] = int(metric_weight)
            set_entry["reps"] = int(metric_rep)
            set_entry["time"] = time.strftime("%H:%M:%S")
            set_entry["duration"] = str((end_time - time).total_seconds())
            print("Duration: " + set_entry["duration"])
            sets.append(set_entry)
            empty_entry = dict()
            empty_entry["time"] = None
            empty_entry["duration"] = None
            empty_entry["weight"] = None
            empty_entry["reps"] = None
            set_entry = empty_entry
        elif set_opt == "0":
            break
    entry_date = str(entry_time.year) + "/" + str(entry_time.month) + "/" + str(entry_time.day)
    new_entry = {
            "date": entry_date,
            "movement": movement_opt,
            "average_metric": calc_avg_metric(sets),
            "sets": sets
            }
    print("\nReview.")
    print(new_entry)
    while True:
        conf_new_entry_input = input("Confirm? (Y/n): ")
        if conf_new_entry_input == "Y" or conf_new_entry_input == "y" or conf_new_entry_input == "":
            break
        elif conf_new_entry_input == "N" or conf_new_entry_input == "n":
            exit()
    data_file["data"].append(new_entry)

def calc_avg_metric(sets):
    same_weight = True
    first_weight = sets[0]["weight"]
    for entry_set in sets:
        if first_weight == entry_set["weight"]:
            continue
        else:
            same_weight = False
            break
    average_weight = None
    if same_weight:
        most_reps = 0
        sum_weight = 0
        for entry_set in sets:
            sum_weight += entry_set["weight"] * entry_set["reps"]
            if entry_set["reps"] > most_reps:
                most_reps = entry_set["reps"]
        average_weight = sum_weight / (most_reps * len(sets))
    else:
        sum_reps = 0
        sum_weight = 0
        for entry_set in sets:
            sum_weight += entry_set["weight"] * entry_set["reps"]
            sum_reps += entry_set["reps"]
        average_weight = sum_weight / sum_reps
    return average_weight

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
elif argv[1] == "add":
    with open(data_filename, "r") as f:
        data_file = json.loads(f.read())
    add_entry(data_file)
    with open(data_filename, "w") as f:
        f.write(json.dumps(data_file))
else:
    print("Error: Unknown argument '" + argv[1] + "'")
    exit()

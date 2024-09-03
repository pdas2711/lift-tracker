import json

exercises = {
                "1": {
                    "name": "Incline Bench Smith",
                    "group": "Chest"
                    },
                "2": {
                    "name": "Seated Pec",
                    "group": "Chest"
                    }
                }

def get_movement_id(movement):
    for index in exercises:
        if exercises[index] == movement:
            return index

def import_csv(data_file, filename):
    with open(filename, "r") as f:
        csv_data = f.readlines()
    header_data = csv_data.pop(0)
    for record in csv_data:
        for col_index, column in enumerate(header_data.split(",")):
            entry = {
                    "date": None,
                    "movement": None,
                    "average_metric": None,
                    "sets": "Not Available"
            }
            if column == "DATE":
                entry["date"] = column
            else:
                entry["movement"] = get_movement_id(column)
                entry["average_metric"] = record.split(",")[col_index]
            data_file["data"].append(entry)

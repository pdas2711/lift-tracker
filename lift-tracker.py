import json

movements = {
                "0": {
                    "name": "Incline Bench Smith",
                    "group": "Chest"
                    },
                "1": {
                    "name": "Seated Pec",
                    "group": "Chest"
                    }
                }

def get_movement_id(movement):
    for index in movements:
        if movements[index]["name"] == movement:
            return index
    return None

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

def generate_data_file(filename):
    data_file = {
            "key": movements,
            "data": []
            }
    with open(filename, "w") as f:
        f.write(json.dumps(data_file))

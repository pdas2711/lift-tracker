import json
from sys import argv

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

def get_movement_id(movements, movement):
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
    set_category = False
    set_location = False
    category = None
    location = None
    for arg in argv:
        if set_category:
            category = arg
            set_category = False
        elif set_location:
            location = arg
            set_location = False
        if arg == "--category":
            set_category = True
        elif arg == "--location":
            set_location = True
    if not category:
        category = input("Category: ")
    if not location:
        location = input("Location: ")
    with open(data_filename, "r") as f:
        data_file = json.loads(f.read())
    import_csv(data_file, argv[-1])
    with open(data_filename, "w") as f:
        f.write(json.dumps(data_file))
else:
    print("Error: Unknown argument '" + argv[1] + "'")
    exit()

import json

def store_json(json_file, output_path):
    with open(output_path, "w") as outfile:
        json.dump(json_file, outfile)
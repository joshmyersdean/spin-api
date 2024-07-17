import json
import os

json_file_path = os.path.join(os.path.dirname(__file__), "object_mapping.json")

with open(json_file_path, "r") as f:
    file_to_object_mapping = json.load(f)[0]

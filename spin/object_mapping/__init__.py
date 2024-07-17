import json

with open("spin/object_mapping/object_mapping.json", "r") as f:
	file_to_object_mapping = json.load(f)[0]

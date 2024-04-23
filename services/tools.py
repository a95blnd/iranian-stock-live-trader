import json


def convert_signal_to_json(data):
    if not data:
        return []

        # Split the data using Unit Separator (ASCII character )
    objects = data.split("")

    # Convert each object to JSON and return as a list
    json_objects = []
    for obj in objects:
        if obj != '':
            try:
                json_obj = json.loads(obj)
                json_objects.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e} --- {obj}")
                continue  # Skip this object if it can't be decoded

    return json_objects

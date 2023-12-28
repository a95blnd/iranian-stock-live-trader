import json
import os


def extract_instrument_ids():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'constants', 'instrument_data.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        instrument_ids = [item["instrumentId"] for item in json_data]
        return instrument_ids
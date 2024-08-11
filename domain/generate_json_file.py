import json


def generate_json_file(filename: str, payload: dict):
    """Generates a non existing `filename` file, with the `payload` as it's content"""
    with open(filename, mode="x") as f:
        f.write(json.dumps(payload, default=str))

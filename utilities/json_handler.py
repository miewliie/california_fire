import os
import json


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as output_file:
        size = os.path.getsize(file_path)
        if size > 0:
            data = json.loads(output_file.read())
        else:
            data = None
        return data


def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file)
        print("Done write response into json file")

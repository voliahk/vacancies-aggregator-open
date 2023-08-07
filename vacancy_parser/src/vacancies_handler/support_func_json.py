from pathlib import Path

import datetime
import json


def load_json_dataset(json_filenames: list):
    try:
        loaded_content = []
        for filename in json_filenames:
            with open(filename, 'r', encoding='utf-16') as file:
                loaded_content += json.loads(file.read())
        return loaded_content
    except FileNotFoundError as e:
        print(e)


def read_directory(directory_path: str):
    paths = sorted(Path(directory_path).glob('*.json'))
    filenames = list(map(str, paths))
    return load_json_dataset(filenames)


def create_json(processed_data, upload_path, prefix: str):
    def generate_filename(prefix: str):
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        generated_name = "_".join([prefix, suffix]) + '.json'
        return generated_name

    filename = generate_filename(prefix)
    with open(upload_path + '/' + filename, 'w', encoding='utf-16') as json_file:
        json.dump(processed_data, json_file, ensure_ascii=False)
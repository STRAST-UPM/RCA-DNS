# external imports
import json
from os import path, makedirs, listdir
# internal imports

def create_directory_structure(path_to_create: str) -> None:
    # Remove files from path, only directories
    if path_to_create[-1] != "/":
        path_to_create = "/".join(path_to_create.split("/")[:-1])
    if path_to_create == "":
        return
    if not path.exists(path_to_create):
        makedirs(path_to_create)


def json_file_to_dict(file_path: str) -> dict:
    create_directory_structure(file_path)
    with open(file_path) as file:
        raw_json = file.read()

    return json.loads(raw_json)


def json_file_to_list(file_path: str) -> list:
    create_directory_structure(file_path)
    with open(file_path) as file:
        raw_json = file.read()

    return json.loads(raw_json)

def json_file_to_set(file_path: str) -> list:
    return set(json_file_to_list(file_path))


def dict_to_json_file(dict_to_save: dict, file_path: str, sort_keys: bool = False):
    create_directory_structure(file_path)
    file = open(file_path, "w")
    file.write(json.dumps(dict_to_save, indent=4, sort_keys=sort_keys))
    file.close()


def list_to_json_file(list_to_save: list, file_path: str):
    create_directory_structure(file_path)
    file = open(file_path, "w")
    file.write(json.dumps(list_to_save, indent=4))
    file.close()

def get_filepaths_from_folder(folder_path: str) -> list[str]:
    filepath_list = []
    for filename in listdir(folder_path):
        filepath = path.join(folder_path, filename)
        if path.isfile(filepath):
            filepath_list.append(filepath)

    return filepath_list

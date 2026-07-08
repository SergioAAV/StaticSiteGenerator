import os
import shutil

def copy_content(source: str, destiny: str) -> None:
    if not os.path.exists(destiny):
        os.mkdir(destiny)
    for file in os.listdir(source):
        path_source = os.path.join(source, file)
        path_destiny = os.path.join(destiny, file)
        print(f" * {path_source} -> {path_destiny}")
        if os.path.isfile(path_source):
            shutil.copy(path_source, path_destiny)
        else:
            copy_content(path_source, path_destiny)
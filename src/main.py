import os
import shutil

from copy_static import copy_content

dir_path_static = "./static"
dir_path_public = "./public"

def main() -> None:
    print("Cleaning public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_content(dir_path_static, dir_path_public)


main()

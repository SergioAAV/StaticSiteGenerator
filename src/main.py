import os
import shutil
import sys

from copy_static import copy_content
from gen_content import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main() -> None:
    if len(sys.argv) > 0:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    print("Cleaning public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_content(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


main()

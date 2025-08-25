import os
import sys
import shutil
from copy_static import copy_files_from_static
from generate_content import generate_pages_recursively

static_path = "./static"
docs_path = "./docs"
content_path = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print("Deleting docs directory...")
    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)
    
    print("Copying files from static to docs...")
    copy_files_from_static(static_path, docs_path)

    print("Generating content...")
    generate_pages_recursively(content_path, template_path, docs_path, basepath)

if __name__ == '__main__':
    main()
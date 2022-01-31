#!.venv/bin/python

import glob
import os
import sys
import shutil

from jinja2 import Environment, FileSystemLoader


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

if not os.path.exists('docs'):
    os.mkdir('docs')

if not os.path.exists('src'):
    print("Cannot find `src` directory!")
    sys.exit(1)

template_loader = Environment(loader=FileSystemLoader("src"))

html_files = glob.glob("src/*.html")
# strip out the folder name
html_files = [f[f.index("/") + 1:] for f in html_files]

static = glob.glob("src/*.css")
static += glob.glob("src/*.js")
static = [f[f.index("/") + 1:] for f in static]

for template in html_files:
    with open(f"src/{template}") as f:
        template_str = f.read()
        result = template_loader.from_string(template_str).render()

    with open(f"docs/{template}", mode="w") as f:
        f.write(result)

for static_file in static:
    with open(f"src/{static_file}") as f:
        template_str = f.read()

    with open(f"docs/{static_file}", mode="w") as f:
        f.write(template_str)

copy_and_overwrite("images", "docs/images")
print("All done!")

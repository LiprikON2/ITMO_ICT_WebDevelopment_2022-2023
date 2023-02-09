#!/bin/bash 
# Makes it so it doesn't matter from which directory script is called
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P ) # https://stackoverflow.com/a/24112741
cd "$parent_path"

source ".docs-venv/Scripts/activate" && mkdocs gh-deploy && git commit -am "mkdocs gh-deploy" && git push

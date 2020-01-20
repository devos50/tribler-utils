import ast
import os
import sys

location = os.path.abspath(sys.argv[1])

exclude_from_check = ['twisted/plugins/tunnel_helper_plugin.py']

for (dirpath, dirnames, filenames) in os.walk(location):
    for filename in filenames:
        if not filename.endswith('.py'):
            continue
        file_contents = ''
        file_path = os.path.join(dirpath, filename)
        if any([file_path.endswith(excluded_path) for excluded_path in exclude_from_check]):
            continue
        with open(file_path, 'r') as file:
            file_contents = file.read()
        if file_contents:
            node = ast.parse(file_contents)
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Call) and hasattr(subnode.func, 'id') and subnode.func.id == "print":
                    print(f"print at line {subnode.lineno}, col {subnode.col_offset} in file {file_path}")

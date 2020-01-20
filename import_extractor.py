import ast
import distutils.sysconfig as sysconfig
import imp
import pathlib
import pkgutil
import os
import sys

built_in_modules = set(sys.builtin_module_names)
built_in_modules.update({
    module
    for _, module, package in pkgutil.iter_modules()
    if package is False
})
std_lib = sysconfig.get_python_lib(standard_lib=True)
for top in pathlib.Path(std_lib).iterdir():
    if str(top).startswith(('dist-packages', 'site-packages')):
        continue
    built_in_modules.add(str(top).split('.')[0])

# We take the top-folder as input
location = os.path.abspath(sys.argv[1])
hint_locations = [os.path.join(location, 'src', 'pyipv8'),
                  os.path.join(location, 'src', 'anydex'),
                  os.path.join(location, 'src', 'tribler-core'),
                  os.path.join(location, 'src', 'tribler-common'),
                  os.path.join(location, 'src', 'tribler-gui')]
external_modules = set()


def is_external_module(top_path, path, name):
    """
    Check if we can import this module from somewhere in the local file structure.
    (Filter out imports within the workspace)
    """
    if not name:
        return
    name = name.split('.')[0]
    if name not in built_in_modules:
        try:
            imp.find_module(name, [os.path.dirname(path), path, top_path] + hint_locations)
        except ImportError:
            external_modules.add(name)


location = os.path.abspath(sys.argv[1])
for dirpath, dirnames, filenames in os.walk(location):
    py_filenames = [filename for filename in filenames if filename.endswith('.py')]
    for filename in py_filenames:
        with pathlib.Path(dirpath, filename).open() as file:
            file_contents = file.read()
        if not file_contents:
            continue
        try:
            node = ast.parse(file_contents)
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Import):
                    for import_name in (alias.name for alias in subnode.names):
                        is_external_module(location, dirpath, import_name)
                if isinstance(subnode, ast.ImportFrom):
                    is_external_module(location, dirpath, subnode.module)
        except:
            print("ERROR: Failed to parse", filename, file=sys.stderr)

for name in sorted(external_modules):
    print(name)

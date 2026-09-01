import os
from collections.abc import Iterator
from pathlib import Path


def is_skippable(dir_name: str) -> bool:
    return dir_name == "node_modules" or dir_name.startswith((".", "__"))


def traverse_file(root: str | Path) -> Iterator[str]:
    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not is_skippable(d)]
        for f in file_names:
            yield os.path.join(dir_path, f)

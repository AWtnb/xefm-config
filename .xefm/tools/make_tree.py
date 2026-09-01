import os
from pathlib import Path

from lib.tree import traverse_file


def main():

    root = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd()))
    lines = [str(Path(p).relative_to(root)) for p in traverse_file(root)]

    out_name = f"tree_{root.name}.txt"
    out_path = Path(os.environ.get("XEFM_OTHER_DIR", os.getcwd())) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

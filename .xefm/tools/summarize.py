import os
import shlex
from pathlib import Path

from lib.tree import is_skippable, traverse_file
from lib.util import get_timestamp


def summarize(root: Path, targets: list[str]) -> tuple[str, int]:
    paths = []
    tree_flag = False
    for path in targets:
        if Path(path).is_dir():
            tree_flag = True
            paths.extend(traverse_file(path))
        else:
            paths.append(path)

    border = "```"
    lines: list[str] = ["# SUMMARY\n"]

    if tree_flag:
        lines.append("## DIRECTORIES\n")
        lines.append(border)
        lines.extend(str(Path(p).relative_to(root)) for p in paths)
        lines.append(f"{border}\n")

    lines.append("## FILE CONTENTS\n")

    counter = 0
    for path in paths:
        p = Path(path)
        try:
            content = p.read_text(encoding="utf-8")
            counter += 1
        except Exception:  # noqa: BLE001, S112
            continue
        lines.append(f"### Content of `{p.relative_to(root)}`\n")
        lines.append(border)
        lines.append(content)
        lines.append(f"{border}\n")

    return "\n".join(lines), counter


def main():

    root = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd()))
    selected_names = shlex.split(os.environ.get("XEFM_THIS_SELECTED", ""))
    if len(selected_names) < 1:
        print("Nothing selected.")
        return

    targets = []
    for name in selected_names:
        path = name if os.path.isabs(name) else os.path.join(root, name)
        p = Path(path)
        if p.is_dir() and is_skippable(p.name):
            continue
        targets.append(path)

    out_name = f"{root.name}_summary_{get_timestamp()}.md"
    md, count = summarize(root, targets)
    out_path = Path(os.environ.get("XEFM_OTHER_DIR", os.getcwd())) / out_name
    out_path.write_text(md, encoding="utf-8")

    print(f"[FINISHED] Summarized {count} files.")


if __name__ == "__main__":
    main()

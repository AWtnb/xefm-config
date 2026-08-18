import datetime
import os
import shlex
from collections.abc import Iterator
from pathlib import Path


def is_skippable(dir_name: str) -> bool:
    return dir_name == "node_modules" or dir_name.startswith((".", "__"))


def traverse_file(root: str) -> Iterator[str]:
    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not is_skippable(d)]
        for f in file_names:
            yield os.path.join(dir_path, f)


def summarize(root: Path, targets: list[str]) -> tuple[str, int]:
    paths = []
    for path in targets:
        if Path(path).is_dir():
            paths.extend(traverse_file(path))
        else:
            paths.append(path)

    codeblock = "```"
    lines: list[str] = ["## dir tree\n", codeblock]
    lines.extend(str(Path(p).relative_to(root)) for p in paths)
    lines.append(codeblock)
    lines.append("\n## file contents\n")

    counter = 0
    for path in paths:
        p = Path(path)
        try:
            content = p.read_text(encoding="utf-8")
            counter += 1
        except Exception:  # noqa: BLE001, S112
            continue
        lines.append(f"### {p.relative_to(root)}\n")
        lines.append(f"{codeblock}{p.name}")
        lines.append(content)
        lines.append(f"{codeblock}\n")

    return "\n".join(lines), counter


def get_timestamp() -> str:
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(tz=tz_jst).strftime("%Y%m%d-%H%M%S")


def main():

    root = Path(os.environ.get("XEFM_THIS_DIR", os.getcwd()))
    selected_names = shlex.split(os.environ.get("XEFM_THIS_SELECTED", ""))
    if len(selected_names) < 1:
        for p in root.iterdir():
            if p.is_dir():
                selected_names.append(str(p))

    targets = [
        (name if os.path.isabs(name) else os.path.join(root, name))
        for name in selected_names
    ]

    out_name = f"{root.name}_summary_{get_timestamp()}.md"
    md, count = summarize(root, targets)
    out_path = Path(os.environ.get("XEFM_OTHER_DIR", os.getcwd())) / out_name
    out_path.write_text(md, encoding="utf-8")

    print(f"[FINISH]Summarized {count} files.")


if __name__ == "__main__":
    main()

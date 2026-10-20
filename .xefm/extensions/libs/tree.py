import os
from collections.abc import Iterator
from pathlib import Path


def is_skippable(dir_name: str) -> bool:
    return dir_name in ("node_modules", ".git") or dir_name.startswith("__")


def traverse_file(root: str | Path) -> Iterator[str]:
    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not is_skippable(d)]
        for f in file_names:
            yield os.path.join(dir_path, f)


def make_tree(ctx) -> None:
    root = Path(ctx.pane.path)
    lines = [str(Path(p).relative_to(root)) for p in traverse_file(root)]
    selected = {ent.name for ent in ctx.pane.selected()}
    if selected:
        lines = [l for l in lines if (l.split(os.sep)[0] in selected)]
    out_name = f"tree_{root.name}.txt"
    out_path = Path(ctx.other.path) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")
    ctx.other.cd(ctx.other.path, out_name)
    ctx.other.activate()


def summarize_by(ctx) -> None:
    selected = ctx.pane.selected()
    if not selected:
        return
    rel_paths = Path(str(selected[0])).read_text(encoding="utf-8").splitlines()

    other_root = Path(ctx.other.path)
    targets = []
    for rel in rel_paths:
        p = other_root / rel
        if p.exists():
            targets.append(p)

    if not targets:
        return

    border = "```"
    lines: list[str] = ["# SUMMARY\n"]
    lines.append("## DIRECTORIES (excerpt)\n")
    lines.append(border)
    lines.extend(rel_paths)
    lines.append(f"{border}\n")

    lines.append("## FILE CONTENTS\n")

    for path in targets:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001, S112
            continue
        lines.append(f"### Content of `{path.relative_to(other_root)}`\n")
        lines.append(border)
        lines.append(content)
        lines.append(f"{border}\n")

    out_name = f"resume_{other_root.name}.md"
    out_path = Path(ctx.pane.path) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")

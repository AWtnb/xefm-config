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


def _get_git_root(path: str) -> Path:
    original = Path(path)
    current = original
    while True:
        if (current / ".git").exists():
            return Path(current)
        if current.parent == current:
            return Path(original)
        current = current.parent


def make_tree(ctx) -> None:
    root = _get_git_root(str(ctx.pane.path))
    lines = [p for p in traverse_file(root)]
    selected = {str(ent.path) for ent in ctx.pane.selected()}
    if selected:
        lines = [l for l in lines if any(l.startswith(s) for s in selected)]
    lines = [str(Path(l).relative_to(root)) for l in lines]
    out_name = f"{Path(root).stem}.tree.txt"
    out_path = Path(ctx.other.path) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")
    ctx.other.cd(ctx.other.path, out_name)


def summarize_by(ctx) -> None:
    selected = ctx.pane.selected()
    if not selected:
        return
    rel_paths = Path(selected[0].path).read_text(encoding="utf-8").splitlines()

    def _summarize(root: str) -> None:
        _, root_name = os.path.split(root)
        targets = []
        for rel in rel_paths:
            p = Path(root, rel)
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

        for i, path in enumerate(targets):
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:  # noqa: BLE001, S112
                continue
            lines.append(f"### Content of `{rel_paths[i]}`\n")
            lines.append(border)
            lines.append(content)
            lines.append(f"{border}\n")

        out_name = f"{root_name}.context.md"
        out_path = Path(ctx.pane.path) / out_name
        out_path.write_text("\n".join(lines), encoding="utf-8")
        ctx.pane.cd(ctx.pane.path, out_name)

    ctx.input(
        prompt="root of summary",
        default=str(_get_git_root(str(ctx.other.path))),
        on_accept=_summarize,
    )

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

from ._utils import get_git_root


def _is_skippable(dir_name: str) -> bool:
    return dir_name in ("node_modules", ".git") or dir_name.startswith("__")


def traverse_file(root: str | Path) -> Iterator[str]:
    for dir_path, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if not _is_skippable(d)]
        for f in file_names:
            yield os.path.join(dir_path, f)


def make_tree(ctx) -> None:
    root = get_git_root(str(ctx.pane.path))
    lines = [p for p in traverse_file(root)]
    selected = {str(ent.path) for ent in ctx.pane.selected()}
    if selected:
        lines = [l for l in lines if any(l.startswith(s) for s in selected)]
    lines = [str(Path(l).relative_to(root).as_posix()) for l in lines]
    out_name = f"{Path(root).stem}.tree.txt"
    out_path = Path(ctx.other.path) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")
    ctx.other.cd(ctx.other.path, out_name)


def summarize(ctx, editor: str | list[str]) -> None:
    pane_path = Path(ctx.pane.path)
    root = get_git_root(str(pane_path))
    rel_paths = [
        Path(path).relative_to(root).as_posix() for path in traverse_file(root)
    ]

    with tempfile.TemporaryDirectory(prefix="xefm-summarize-") as temp_dir:
        tree_path = Path(temp_dir) / f"{root.name}.tree.txt"
        tree_path.write_text("\n".join(rel_paths), encoding="utf-8")
        command = [editor] if isinstance(editor, str) else editor
        ctx.run_program(
            [*command, str(tree_path)],
            terminal=True,
            cwd=str(root),
        )
        rel_paths = tree_path.read_text(encoding="utf-8").splitlines()

    if not _write_context(ctx, root, ctx.other.path, rel_paths):
        ctx.message("No files to summarize.")


def _write_context(
    ctx,
    root: str | Path,
    output_dir: str | Path,
    rel_paths: list[str],
) -> bool:
    root_path = Path(root).resolve()
    targets = []
    for rel in rel_paths:
        candidate = Path(rel)
        if candidate.is_absolute():
            ctx.message(f"Skipping absolute path in tree: {rel}")
            continue

        path = (root_path / candidate).resolve()
        try:
            path.relative_to(root_path)
        except ValueError:
            ctx.message(f"Skipping path outside summary root: {rel}")
            continue

        if path.is_file():
            targets.append((rel, path))

    if not targets:
        return False

    _, root_name = os.path.split(root_path)
    if not root_name:
        root_name = root_path.anchor
    border = "```"

    lines: list[str] = [f"# CONTEXT of `{root_name}`\n"]
    lines.append("## DIRECTORIES (excerpt)\n")
    lines.append(f"root: `{root_name}`\n")
    lines.append(border)
    lines.extend(rel_paths)
    lines.append(f"{border}\n")
    lines.append("## FILE CONTENTS\n")

    for rel, path in targets:
        try:
            content = (
                "(env file)"
                if ".env" in path.stem
                else path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError) as exc:
            ctx.message(f"Could not read {rel}: {exc}")
            continue

        lines.append(f"### `{rel}`:\n")
        lines.append(border)
        lines.append(content)
        lines.append(f"{border}\n")

    out_name = f"{root_name}.context.md"
    out_path = Path(output_dir) / out_name
    out_path.write_text("\n".join(lines), encoding="utf-8")
    ctx.pane.cd(output_dir, out_name)
    return True


def summarize_by(ctx) -> None:
    selected = ctx.pane.selected()
    if not selected:
        return
    rel_paths = Path(selected[0].path).read_text(encoding="utf-8").splitlines()

    def _summarize(root: str | None) -> None:
        if root is None:
            return

        _write_context(ctx, root, ctx.pane.path, rel_paths)

    ctx.input(
        prompt="root of summary",
        default=str(get_git_root(str(ctx.other.path))),
        on_accept=_summarize,
    )

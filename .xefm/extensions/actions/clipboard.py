from pathlib import Path

from ._utils import get_git_root, get_selected_or_focused


def _as_codeblock(root: Path, path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    border = "```"
    return f"\n\n{border}{path.relative_to(root)}\n{content}\n{border}"


def smart_copy(ctx) -> None:
    target = get_selected_or_focused(ctx)

    options = ["Fullname", "Name"]
    if not all(e.is_dir for e in target):
        options.append("BaseName")
    options.append("Codeblock")
    options.append("Entry")

    def _copy(i: int | None) -> None:
        if i is None:
            return

        sel = options[i]
        if sel == "Fullname":
            ctx.copy_text("\n".join(str(e.path) for e in target))
            return

        if sel == "Name":
            ctx.copy_text("\n".join(e.name for e in target))
            return

        if sel == "BaseName":
            ctx.copy_text("\n".join(e.path.stem for e in target))
            return

        if sel == "Codeblock":
            git_root = get_git_root(ctx.pane.path)
            ctx.copy_text("\n".join(_as_codeblock(git_root, e.path) for e in target))
            return

        ctx.invoke("clipboard_copy")

    ctx.choose(title="Copy:", items=options, on_result=_copy)

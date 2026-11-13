from datetime import datetime
from pathlib import Path

from PIL import ImageGrab  # ty: ignore[import-not-found]

from ._utils import get_git_root, get_selected_or_focused


def _as_codeblock(root: Path, path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    border = "```"
    return f"\n\n{border}{path.relative_to(root)}\n{content}\n{border}\n\n"


def smart_copy(ctx) -> None:
    target = get_selected_or_focused(ctx)

    options = ["Path", "Name"]

    if not all(e.is_dir for e in target):
        options.append("Basename")

    git_root = get_git_root(ctx.pane.path)
    if str(git_root) != ctx.pane.path:
        options.append("Relative path")

    options.append("Codeblock")
    options.append("Entry")

    def _copy(i: int | None) -> None:
        if i is None:
            return

        sel = options[i]
        if sel == "Path":
            ctx.copy_text("\n".join(str(e.path) for e in target))
            return

        if sel == "Name":
            ctx.copy_text("\n".join(e.name for e in target))
            return

        if sel == "Basename":
            ctx.copy_text("\n".join(e.path.stem for e in target))
            return
        if sel == "Relative path":
            ctx.copy_text("\n".join(str(e.path.relative_to(git_root)) for e in target))
            return

        if sel == "Codeblock":
            ctx.copy_text(
                "\n".join(
                    _as_codeblock(git_root, e.path) for e in target if not e.is_dir
                )
            )
            return

        ctx.invoke("clipboard_copy")

    ctx.choose(title="Copy:", items=options, on_result=_copy)


def save_image_on_clipboard(ctx) -> None:
    pane = ctx.pane
    base = pane.path

    img = ImageGrab.grabclipboard()
    if not img or isinstance(img, list):
        ctx.message("No image data on clipboard")
        return

    save_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
    save_path = Path(base) / save_name
    img.save(save_path)
    ctx.pane.cd(base, focus_name=save_name)

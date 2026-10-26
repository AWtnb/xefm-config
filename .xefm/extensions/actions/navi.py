import os
from pathlib import Path

DESKTOP_PATH = Path(os.path.expanduser(r"~/Desktop"))


def open_desktop(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)
    ctx.other.cd(DESKTOP_PATH)
    ctx.invoke("reset_pane_boundary")


def open_desktop_to_other(ctx) -> None:
    current_path = ctx.pane.path
    other_path = ctx.other.path
    if DESKTOP_PATH not in [current_path, other_path]:
        ctx.other.cd(DESKTOP_PATH)
    ctx.other.activate()


def open_parent_to_other(ctx) -> None:
    parent, current_name = os.path.split(ctx.pane.path)
    ctx.other.cd(parent, current_name)
    ctx.other.activate()


def open_to_other(ctx) -> None:
    if ctx.pane.focused.is_dir:
        ctx.other.cd(ctx.pane.focused)
        ctx.other.activate()

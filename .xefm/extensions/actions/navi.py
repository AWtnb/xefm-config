import os
from pathlib import Path

from xefm import netmount  # ty: ignore[unresolved-import]

from ._utils import get_git_root

DESKTOP_PATH = Path.home() / "Desktop"


def open_desktop(ctx) -> None:
    if ctx.pane.path != (DESKTOP_PATH):
        ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    for pane in [ctx.pane, ctx.other]:
        if pane.path != DESKTOP_PATH:
            pane.cd(DESKTOP_PATH)
    ctx.invoke("reset_pane_boundary")
    ctx.invoke("focus_left")


def open_desktop_to_other(ctx) -> None:
    current_path = ctx.pane.path
    other_path = ctx.other.path
    if DESKTOP_PATH not in [current_path, other_path]:
        ctx.other.cd(DESKTOP_PATH)
    ctx.other.activate()


def open_desktop_to_new_tab(ctx) -> None:
    ctx.invoke("new_tab")
    ctx.pane.cd(DESKTOP_PATH)


def open_parent_to_other(ctx) -> None:
    parent, current_name = os.path.split(ctx.pane.path)
    ctx.other.cd(parent, current_name)
    ctx.other.activate()


def open_parent_to_new_tab(ctx) -> None:
    parent, current_name = os.path.split(ctx.pane.path)
    ctx.invoke("new_tab")
    ctx.pane.cd(parent, current_name)


def open_to_other(ctx) -> None:
    if ctx.pane.focused.is_dir:
        ctx.other.cd(ctx.pane.focused)
        ctx.other.activate()


def eject_current_drive(ctx) -> None:
    path = Path(ctx.pane.path)
    anchor = str(path.anchor)
    mount = netmount.classify(anchor)
    if mount is None or mount.kind != netmount.REMOVABLE:
        return

    def _eject(ok: bool) -> None:
        if ok:
            ctx.pane.cd(DESKTOP_PATH)
            ctx._app._drive_remove({"path": anchor})

    ctx.confirm(f"Eject current drive({path.drive})?", on_result=_eject)


def go_git_root(ctx) -> None:
    path = ctx.pane.path
    if (git_root := get_git_root(path)) != path:
        ctx.pane.cd(git_root)

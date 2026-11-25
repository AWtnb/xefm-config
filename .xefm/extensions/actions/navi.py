import os
from pathlib import Path

from xefm import netmount  # ty: ignore[unresolved-import]

from ._utils import get_git_root, is_image_file


def smart_enter(ctx) -> None:
    if not ctx.pane.focused:
        return

    sels = ctx.pane.selected()
    if sels and all(s.is_file for s in sels):
        ctx.invoke("open_items_with_os")
        return

    focus_path = ctx.pane.focused.path
    ext = focus_path.suffix.lower()
    if focus_path.is_dir() or ext == ".zip":
        ctx.invoke("open_item")
        return

    if ext in [".pdf", ".tbx", ".cmx", ".pptx"]:
        ctx.invoke("open_with_os")
        return

    if ext in [".docx", ".xlsx"] or is_image_file(focus_path.name):
        ctx.invoke("view_file")
        return

    if ctx._app._quick_view:
        ctx._app._close_quick_view()
        ctx.invoke("open_item")
        return

    ctx.invoke("quick_view")


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

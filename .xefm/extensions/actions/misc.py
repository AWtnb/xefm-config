import os

from .item_selector import select_under_cursor

DESKTOP_PATH = os.path.expanduser(r"~/Desktop")


def open_in_vscode(ctx) -> None:
    """Open current dir in VS Code."""
    ctx.run_program(["code", str(ctx.pane.path)])


def quick_copy(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("copy_files")


def quick_move(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("move_files")


def open_desktop(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)
    ctx.other.cd(DESKTOP_PATH)
    ctx.invoke("reset_pane_boundary")

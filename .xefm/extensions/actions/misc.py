import os
import shutil

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


def launch_config_repo(ctx) -> None:
    config_path = os.path.expanduser(r"~\.xefm")
    if not os.path.exists(config_path):
        print(f"config not found: {config_path}")
        return

    dir_path = config_path
    if (real_path := os.path.realpath(config_path)) != dir_path:
        dir_path = os.path.dirname(real_path)

    cmd = ["explorer.exe", dir_path]
    if (vscode_path := shutil.which("code")) is not None:
        cmd[0] = vscode_path

    ctx.run_program(cmd)

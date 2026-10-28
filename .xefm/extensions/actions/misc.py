import os
import shutil
import subprocess

from .item_selector import select_under_cursor


def open_in_vscode(ctx) -> None:
    """Open current dir in VS Code."""
    ctx.run_program(["code", str(ctx.pane.path)])


def open_in_smoothcsv(ctx) -> None:
    """Open item in SmoothCSV"""
    smooth_csv_path = r"C:\Program Files\SmoothCSV\smoothcsv-cli.exe"
    if not os.path.exists(smooth_csv_path):
        ctx.message("SmoothCSV not found...")
        return

    target = ctx.pane.selected() or [ctx.pane.focused]
    for entry in target:
        if entry.path.suffix in [".csv", ".txt"]:
            ctx.run_program([smooth_csv_path, str(entry.path)])


def quick_copy(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("copy_files")


def quick_move(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("move_files")


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


def launch_recycle_bin(_) -> None:
    subprocess.run(["explorer.exe", "shell:RecycleBinFolder"], check=False)

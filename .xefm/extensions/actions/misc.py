import os
import shutil
import subprocess

from ._utils import get_selected_or_focused
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

    target = get_selected_or_focused(ctx)
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


def conc_pdf(ctx) -> None:
    exe_name = "go-pdfconc.exe"
    exe_path = shutil.which(exe_name)
    if not exe_path:
        ctx.message(f"'{exe_name}' not found!")
        return

    selected = [ent for ent in ctx.pane.selected() if ent.path.suffix.lower() == ".pdf"]
    if len(selected) < 2:
        return

    target = [str(ent.path) for ent in selected]

    def _conc(out_name: str | None) -> None:
        if out_name is None:
            return

        out_name = out_name.removesuffix(".pdf")

        def _work(_) -> None:
            cmd = [exe_path, "--outname", out_name]
            try:
                subprocess.run(
                    cmd,
                    input="\n".join(target),
                    capture_output=True,
                    encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=True,
                )
            except Exception as e:  # noqa: BLE001
                raise RuntimeError(str(e))

        ctx.run_task(
            title="Concatenate PDFs",
            work=_work,
            on_done=lambda c, outcome: (
                c.message("PDF concatenation finished.")
                if outcome.ok
                else c.message(f"PDF concatenation failed: {outcome.error}")
            ),
        )

    ctx.input(
        prompt="Concatenated file name:",
        default="conc",
        title="Concatenate PDFs",
        on_accept=_conc,
    )

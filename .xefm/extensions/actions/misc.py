import configparser
import os
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

from ._utils import get_selected_or_focused
from .item_selector import select_under_cursor


def smart_mkdir(ctx) -> None:
    pane = ctx.pane
    base = pane.path
    today = datetime.now().strftime("%Y%m%d")

    def _mkdir(name: str) -> None:
        new_path = base / name
        if new_path.exists():
            ctx.message(f"Path already exists: '{new_path}'")
            return

        new_path.mkdir()
        pane.cd(base, focus_name=name)

    ctx.input("Directory name", default=today, on_accept=_mkdir)


def lazygit(ctx) -> None:
    lazygit_path = shutil.which("lazygit")
    if lazygit_path is None:
        ctx.message("lazygit not found.")
        return
    ctx.run_program(
        [lazygit_path],
        terminal=True,
        cwd=str(ctx.pane.path),
    )


def diffinity(ctx) -> None:
    diffinity_exe = shutil.which("diffinity")
    if diffinity_exe is None:
        ctx.message("diffinity not found")
        return

    def _get_paths() -> tuple[str, str] | None:
        l_sels = ctx.left.selected()
        r_sels = ctx.right.selected()
        if len(l_sels) == 1 and len(r_sels) == 1:
            l = l_sels[0]
            r = r_sels[0]
            if not l.is_dir and not r.is_dir:
                return str(l.path), str(r.path)

        sels = ctx.pane.selected()
        if len(sels) == 2:
            l, r = sels
            if not l.is_dir and not r.is_dir:
                return str(l.path), str(r.path)

        return None

    paths = _get_paths()
    if paths is None:
        ctx.message("Select just 2 files")
        return

    l_path, r_path = paths
    ctx.run_program([diffinity_exe, l_path, r_path])


def open_in_vscode(ctx) -> None:
    """Open current dir in VS Code."""
    ctx.run_program(["code", str(ctx.pane.path)])


def open_with_smoothcsv(ctx) -> None:
    """Open item with SmoothCSV"""
    smooth_csv_path = "C:/Program Files/SmoothCSV/smoothcsv-cli.exe"
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
    config_path = Path.home() / ".xefm"
    if not config_path.exists():
        print(f"config not found: {config_path}")
        return

    dir_path = config_path
    if (real_path := config_path.resolve()) != dir_path:
        dir_path = real_path.parent

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


def open_git_remote(ctx) -> None:
    dirs = [e for e in get_selected_or_focused(ctx) if e.is_dir]
    if not dirs:
        return

    for d in dirs:
        git_path = d.path / ".git"
        if not git_path.exists():
            continue

        config_path = git_path / "config"
        if not config_path.is_file():
            continue

        config = configparser.ConfigParser(interpolation=None)
        try:
            config.read_string(config_path.read_text(encoding="utf-8"))
        except (OSError, configparser.Error):
            continue

        remote_url = config.get('remote "origin"', "url", fallback="").strip()
        if 2 <= len(remote_url) and remote_url[0] == remote_url[-1] == '"':
            remote_url = remote_url[1:-1]

        if remote_url:
            webbrowser.open(remote_url)

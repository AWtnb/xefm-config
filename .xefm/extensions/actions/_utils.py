import shutil
import subprocess
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from pathlib import Path

from xefm.user_api import is_desktop_mode  # ty: ignore[unresolved-import]


def smart_check_path(path: str | Path, timeout_sec: float | None = None) -> bool:
    """CASE-INSENSITIVE path check with timeout"""
    p = path if isinstance(path, Path) else Path(path)
    try:
        future = ThreadPoolExecutor(max_workers=1).submit(p.exists)
        return future.result(timeout_sec)
    except Exception:  # noqa: BLE001
        return False


def get_git_root(path: str) -> Path:
    original = Path(path)
    current = original
    while True:
        if (current / ".git").exists():
            return Path(current)
        if current.parent == current:
            return Path(original)
        current = current.parent


def get_selected_or_focused(ctx) -> list:
    return ctx.pane.selected() or [ctx.pane.focused]


def is_nfd(entry):
    return not unicodedata.is_normalized("NFC", entry.path.name)


def fzf_filter(ctx, options: list[str], multi: bool) -> list[str]:
    fzf = shutil.which("fzf")
    if fzf is None:
        ctx.message("fzf not found")
        return []

    desktop_mode = is_desktop_mode()
    terminal_context = (
        nullcontext() if desktop_mode else ctx.terminal_backend_suspended()
    )
    program_env = {} if desktop_mode else ctx.program_env()

    cmd = [fzf]
    if multi:
        cmd.append("--multi")

    # https://github.com/crftwr/xefm/issues/755
    with terminal_context:
        r = subprocess.run(
            cmd,
            input="\n".join(options),
            encoding="utf-8",
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if desktop_mode else None,
            **program_env,
        )

    if r.returncode in (1, 130):
        return []

    return r.stdout.strip().splitlines()


def focus_by_name(ctx, name: str) -> None:
    for i, ent in enumerate(ctx.pane.entries):
        if ent.name == name:
            ctx.pane.cursor = i
            return

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


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

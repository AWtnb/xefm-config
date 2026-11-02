"""
https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
"""

import os
import shutil
import subprocess
from contextlib import nullcontext
from pathlib import Path

from xefm import favorites  # ty: ignore[unresolved-import]
from xefm.user_api import is_desktop_mode  # ty: ignore[unresolved-import]


def fuzzy_ghq(ctx) -> None:
    ghq_root = Path(os.path.expanduser(r"~/ghq"))
    if not ghq_root.is_dir():
        ctx.message(f"ghq root not found: {ghq_root}")
        return

    fzf_cmd = shutil.which("fzf")
    if fzf_cmd is None:
        ctx.message("fzf not found")
        return

    repo_roots = [p for p in ghq_root.glob("*/*/*") if p.is_dir()]
    if not repo_roots:
        ctx.message("No repositories found under ~/ghq.")
        return

    repo_paths = {}
    for path in repo_roots:
        rel = path.relative_to(ghq_root)
        repo_paths[str(rel)] = str(path)

    desktop_mode = is_desktop_mode()
    terminal_context = (
        nullcontext() if desktop_mode else ctx.terminal_backend_suspended()
    )
    program_env = {} if desktop_mode else ctx.program_env()

    # https://github.com/crftwr/xefm/issues/755
    with terminal_context:
        r = subprocess.run(
            [fzf_cmd],
            input="\n".join(repo_paths.keys()),
            encoding="utf-8",
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if desktop_mode else None,
            **program_env,
        )

    if r.returncode in (1, 130):
        return

    selected = r.stdout.strip()
    if not selected:
        return

    ctx.pane.cd(repo_paths[selected])


def fuzzy_favorites(ctx) -> None:
    fzf_cmd = shutil.which("fzf")
    if fzf_cmd is None:
        ctx.message("fzf not found")
        return

    favs = {
        f.name: f.path
        for f in favorites.get_favorites()  # list[FavoriteEntry]
    }

    desktop_mode = is_desktop_mode()
    terminal_context = (
        nullcontext() if desktop_mode else ctx.terminal_backend_suspended()
    )
    program_env = {} if desktop_mode else ctx.program_env()

    # https://github.com/crftwr/xefm/issues/755
    with terminal_context:
        r = subprocess.run(
            [fzf_cmd],
            input="\n".join(favs.keys()),
            encoding="utf-8",
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if desktop_mode else None,
            **program_env,
        )

    if r.returncode in (1, 130):
        return

    selected = r.stdout.strip()
    if not selected:
        return

    path = Path(favs[selected])
    if path.is_dir():
        ctx.pane.cd(path, focus_name=None)
    else:
        ctx.pane.cd(path.parent, focus_name=path.name)

    ctx.pane.refresh()

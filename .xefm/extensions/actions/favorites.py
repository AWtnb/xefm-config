"""
https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
"""

import os
import shutil
from pathlib import Path

from xefm import favorites  # ty: ignore[unresolved-import]

from ._utils import fzf_filter


def fuzzy_ghq(ctx) -> None:
    ghq_root = Path(os.path.expanduser(r"~/ghq"))
    if not ghq_root.is_dir():
        ctx.message(f"ghq root not found: {ghq_root}")
        return

    repo_roots = [p for p in ghq_root.glob("*/*/*") if p.is_dir()]
    if not repo_roots:
        ctx.message("No repositories found under ~/ghq.")
        return

    repo_paths = {}
    for path in repo_roots:
        rel = path.relative_to(ghq_root)
        repo_paths[str(rel)] = str(path)

    selected = fzf_filter(ctx, list(repo_paths), multi=False)
    if len(selected) == 1:
        ctx.pane.cd(repo_paths[selected[0]])


def fuzzy_favorites(ctx) -> None:
    fzf_cmd = shutil.which("fzf")
    if fzf_cmd is None:
        ctx.message("fzf not found")
        return

    favs = {
        f"{f.name} - {f.path}": f.path
        for f in favorites.get_favorites()  # list[FavoriteEntry]
    }

    selected = fzf_filter(ctx, list(favs), multi=False)
    if len(selected) != 1:
        return

    path = Path(favs[selected[0]])
    if path.is_dir():
        ctx.pane.cd(path, focus_name=None)
    else:
        ctx.pane.cd(path.parent, focus_name=path.name)

    ctx.pane.refresh()

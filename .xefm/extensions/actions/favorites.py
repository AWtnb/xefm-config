"""
https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import NamedTuple

from xefm import favorites  # ty: ignore[unresolved-import]


def open_ghq_repo(ctx) -> None:
    ghq_root = Path(os.path.expanduser(r"~/ghq"))
    if not ghq_root.is_dir():
        ctx.message(f"ghq root not found: {ghq_root}")
        return

    repo_roots: list[Path] = sorted(p for p in ghq_root.glob("*/*/*") if p.is_dir())

    class RepoPath(NamedTuple):
        rel: str
        full: str

        @classmethod
        def from_path(cls, path: Path):
            rel = path.relative_to(ghq_root)
            return cls(str(rel), str(path))

    repo_paths = [RepoPath.from_path(p) for p in repo_roots]
    if not repo_paths:
        ctx.message("No repositories found under ~/ghq.")
        return

    def _on_select(index):
        if index is None:
            return
        ctx.pane.cd(repo_paths[index].full)

    ctx.choose(
        "Select ghq repository",
        [r.rel for r in repo_paths],
        type="filter",
        on_result=_on_select,
    )


def fuzzy_favorites(ctx) -> None:
    fzf_cmd = shutil.which("fzf")
    if fzf_cmd is None:
        ctx.message("fzf not found")
        return

    favs = {
        f.name: f.path
        for f in favorites.get_favorites()  # list[FavoriteEntry]
    }
    names = "\n".join(favs.keys())

    completed = subprocess.run(
        [fzf_cmd],
        input=names,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode in (1, 130):
        return

    selected = completed.stdout.strip()
    if not selected:
        return

    path = Path(favs[selected])
    if path.is_dir():
        ctx.pane.cd(path, focus_name=None)
    else:
        ctx.pane.cd(path.parent, focus_name=path.name)

    ctx.pane.refresh()

"""
https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
"""

import shutil
import unicodedata
from pathlib import Path
from typing import NamedTuple

from xefm import favorites  # ty: ignore[unresolved-import]

from ._utils import fzf_filter


def fuzzy_ghq(ctx) -> None:
    ghq_root = Path.home() / "ghq"
    if not ghq_root.is_dir():
        ctx.message(f"ghq root not found: {ghq_root}")
        return

    repo_roots = [p for p in ghq_root.glob("*/*/*") if p.is_dir()]
    if not repo_roots:
        ctx.message(f"No repositories found under '{ghq_root}'")
        return

    repo_paths = {}
    for path in repo_roots:
        rel = path.relative_to(ghq_root)
        repo_paths[str(rel)] = str(path)

    selected = fzf_filter(ctx, list(repo_paths), multi=False)
    if len(selected) == 1:
        ctx.pane.cd(repo_paths[selected[0]])


def _width_of(text: str) -> int:
    """Return terminal display width, counting wide chars as 2."""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in text)


NAME_COLUMN_WIDTH = 24
ANSI_NAME = "\x1b[36m"
ANSI_RESET = "\x1b[0m"
ELLIPSIS = "..."


def _truncate(text: str) -> str:
    """Truncate text to fit the display width, adding an ellipsis if cut."""
    if _width_of(text) <= NAME_COLUMN_WIDTH:
        return text

    limit = NAME_COLUMN_WIDTH - len(ELLIPSIS)
    result = ""
    used = 0
    for c in text:
        w = _width_of(c)
        if limit < used + w:
            break
        result += c
        used += w
    return result + ELLIPSIS


class FavoriteLine(NamedTuple):
    """A favorite entry rendered as an aligned fzf line."""

    name: str
    path: str

    @property
    def shown_name(self) -> str:
        """Name truncated to the column width."""
        return _truncate(self.name)

    def render(self, colored: bool) -> str:
        """Build the aligned line, optionally with ANSI colors."""
        name = self.shown_name
        padding = " " * (NAME_COLUMN_WIDTH - _width_of(name))
        if colored:
            name = f"{ANSI_NAME}{name}{ANSI_RESET}"
        return f"{name}{padding}  {self.path}"

    @property
    def plain(self) -> str:
        """Line without ANSI codes, used as lookup key."""
        return self.render(colored=False)

    @property
    def colored(self) -> str:
        """Line with ANSI codes, passed to fzf."""
        return self.render(colored=True)


def fuzzy_favorites(ctx) -> None:
    fzf_cmd = shutil.which("fzf")
    if fzf_cmd is None:
        ctx.message("fzf not found")
        return

    items = [FavoriteLine(f.name, str(f.path)) for f in favorites.get_favorites()]
    if not items:
        return

    lookup = {item.plain: item.path for item in items}

    selected = fzf_filter(
        ctx,
        [item.colored for item in items],
        multi=False,
        extra_args=["--ansi"],
    )
    if len(selected) != 1:
        return

    path = Path(lookup[selected[0]])
    if path.is_dir():
        ctx.pane.cd(path, focus_name=None)
    else:
        ctx.pane.cd(path.parent, focus_name=path.name)

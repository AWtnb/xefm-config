from collections.abc import Callable
from itertools import groupby
from typing import NamedTuple

from xefm import (  # ty: ignore[unresolved-import]
    favorites,
    name_key,
)


class SortScore(NamedTuple):
    timestamp: str
    item_index: int


def _make_scorer(file_info) -> Callable[[int, str], SortScore | None]:
    """
    Create a function that returns (date_str, comparison name, index) from file_info.
    Items without date information return None.
    """

    def _score(i, item) -> SortScore | None:
        meta = file_info.get(str(item))
        if not meta:
            return None
        date_str = meta.get("date_str")
        if not date_str:
            return None
        name = meta.get("cmp_name") or name_key.compare_name(item)
        name_key.nfc(name)
        return SortScore(date_str, i)

    return _score


def focus_newest_item(ctx):
    pane = ctx.pane._pane
    items = pane.get("files")
    if not items:
        return

    file_info = pane.get("file_info")
    if not file_info:
        return

    _score = _make_scorer(file_info)
    scores = [_score(i, item) for i, item in enumerate(items)]
    best = max((s for s in scores if s is not None), default=None)
    if best is None:
        return

    ctx.pane.cursor = best.item_index


def focus_older_item(ctx):
    pane = ctx.pane._pane
    items = pane.get("files")
    if not items:
        return

    file_info = pane.get("file_info")
    if not file_info:
        return

    current_index = ctx.pane.cursor
    if current_index < 0:
        return

    _score = _make_scorer(file_info)
    current_score = _score(current_index, items[current_index])
    if current_score is None:
        return

    scores = [_score(i, item) for i, item in enumerate(items)]
    older = [s for s in scores if (s is not None and s < current_score)]
    best = max(older, default=None)
    if best is None:
        return

    ctx.pane.cursor = best.item_index


class JumpCandidates:
    """
    Compute cursor jump candidates for the current pane.
    """

    def __init__(self, ctx) -> None:
        self.pane_info = ctx.pane._pane
        self.items = self.pane_info.get("files") or []
        self.cursor = ctx.pane.cursor

    def get(self) -> set[int]:
        """
        Return jump candidate indices, taking selection and cursor into account.
        """
        if not self.items:
            return set()

        base = self._base_candidates()

        runs = self._selection_runs()
        if not runs:
            return base

        sel_top = runs[0][0]
        sel_bottom = runs[-1][1]

        if self.cursor < sel_top:
            return {i for i in base if i <= sel_top} | {sel_top}

        if sel_bottom < self.cursor:
            return {i for i in base if sel_bottom <= i} | {sel_bottom}

        edges = set()
        for start, end in runs:
            edges.add(start)
            edges.add(end)
        return edges

    def _selection_runs(self) -> list[tuple[int, int]]:
        """
        Return (start, end) index pairs of contiguous selected runs.
        """
        selection_info = self.pane_info.get("selected_files")
        if not selection_info:
            return []

        indices = [
            i for i, item in enumerate(self.items) if str(item) in selection_info
        ]
        runs = []
        for _, group in groupby(enumerate(indices), key=lambda p: p[1] - p[0]):
            run = [idx for _, idx in group]
            runs.append((run[0], run[-1]))
        return runs

    def _base_candidates(self) -> set[int]:
        """
        Return default jump candidates: both ends, dir/file boundary, favorites.
        """
        file_info = self.pane_info.get("file_info")
        if not file_info:
            return set()

        # 1) top / end
        candidates = {0, len(self.items) - 1}

        # 2) end of dirs / top of files
        last_dir = None
        first_file = None
        for i, item in enumerate(self.items):
            meta = file_info.get(str(item))
            if not meta:
                continue
            if meta.get("is_dir"):
                last_dir = i
                continue
            if first_file is None:
                first_file = i

        if last_dir is not None:
            candidates.add(last_dir)
        if first_file is not None:
            candidates.add(first_file)

        # 3) favorites
        fav_paths = {f.path for f in favorites.get_favorites()}
        for i, item in enumerate(self.items):
            if str(item) in fav_paths:
                candidates.add(i)

        return candidates


def _jump_cursor(ctx, down: bool) -> None:
    candidates = JumpCandidates(ctx).get()
    if not candidates:
        return

    current = ctx.pane.cursor
    ordered = sorted(candidates)
    if down:
        target = next((idx for idx in ordered if current < idx), ordered[-1])
    else:
        target = next((idx for idx in reversed(ordered) if idx < current), ordered[0])

    ctx.pane.cursor = target


def jump_down(ctx) -> None:
    _jump_cursor(ctx, True)


def jump_up(ctx) -> None:
    _jump_cursor(ctx, False)

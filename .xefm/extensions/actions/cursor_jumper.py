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


def _get_jump_candidates(ctx) -> set[int]:
    pane_info = ctx.pane._pane
    candidates = set()

    items = pane_info.get("files")
    if not items:
        return candidates

    file_info = pane_info.get("file_info")
    if not file_info:
        return candidates

    #  if selected, edge of selections
    selection_info = pane_info.get("selected_files")
    if selection_info:
        indices = [i for i, item in enumerate(items) if str(item) in selection_info]
        for _, group in groupby(enumerate(indices), key=lambda p: p[1] - p[0]):
            run = [idx for _, idx in group]
            candidates.add(run[0])
            candidates.add(run[-1])
        return candidates

    # 1) top / end
    candidates.add(0)
    candidates.add(len(items) - 1)

    # 2) end of dirs / top of files
    last_dir = None
    first_file = None
    for i, item in enumerate(items):
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
    for i, item in enumerate(items):
        if str(item) in fav_paths:
            candidates.add(i)

    return candidates


def _jump_cursor(ctx, down: bool) -> None:
    candidates = _get_jump_candidates(ctx)
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

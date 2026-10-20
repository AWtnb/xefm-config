from xefm import (  # ty: ignore[unresolved-import]
    favorites,
    name_key,
)


def focus_newest_item(ctx):
    pane = ctx.pane._pane
    items = pane.get("files")
    if not items:
        return

    file_info = pane.get("file_info")
    if not file_info:
        return

    best_index = None
    best_rank = None

    for i, item in enumerate(items):
        meta = file_info.get(str(item))
        if not meta:
            continue
        date_str = meta.get("date_str")
        if not date_str:
            continue

        name = meta.get("cmp_name") or name_key.compare_name(item)

        rank = (date_str, name_key.nfc(name))
        if best_rank is None or best_rank < rank:
            best_rank = rank
            best_index = i

    if best_index is not None:
        ctx.pane.cursor = best_index


def _jump_focus(ctx, down: bool) -> None:
    pane = ctx.pane._pane
    items = pane.get("files")
    if not items:
        return

    file_info = pane.get("file_info")
    if not file_info:
        return

    current = pane.get("focused_index", 0)

    candidates = set()

    # 1) 最初 / 最後
    candidates.add(0)
    candidates.add(len(items) - 1)

    # 2) ディレクトリ最後 / ファイル最初
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

    # 3) favorite を持つ項目
    fav_paths = {f.path for f in favorites.get_favorites()}
    for i, item in enumerate(items):
        if str(item) in fav_paths:
            candidates.add(i)

    ordered = sorted(candidates)
    if down:
        target = next((idx for idx in ordered if current < idx), ordered[-1])
    else:
        target = next((idx for idx in reversed(ordered) if idx < current), ordered[0])

    ctx.pane.cursor = target


def jump_down(ctx) -> None:
    _jump_focus(ctx, True)


def jump_up(ctx) -> None:
    _jump_focus(ctx, False)

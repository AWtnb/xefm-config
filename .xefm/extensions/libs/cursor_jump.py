from xefm import name_key  # ty: ignore[unresolved-import]


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

from ._utils import fzf_filter, is_nfd


# https://github.com/crftwr/xefm/wiki/Spot-NFD-File-Names
def select_nfd_names(ctx):
    """Select the items whose names are stored decomposed (NFD)."""
    n = ctx.pane.select(is_nfd)
    ctx.message(f"Selected {n} NFD name(s)")


def select_under_cursor(ctx) -> None:
    ctx.pane.select(lambda ent: ent.path == ctx.pane.focused.path)


def select_only_files(ctx) -> None:
    ctx.pane.select(lambda ent: not ent.is_dir)


def select_only_dirs(ctx) -> None:
    ctx.pane.select(lambda ent: ent.is_dir)


def _select_by_focus(ctx) -> None:
    focused = ctx.pane.focused
    if focused.is_dir:
        select_only_dirs(ctx)
    else:
        select_only_files(ctx)


def smart_select_all(ctx) -> None:
    selected = ctx.pane.selected()

    if not selected:
        _select_by_focus(ctx)
        return

    if len(selected) == len(ctx.pane.entries):
        return

    selected_paths = [ent.path for ent in selected]
    dir_paths = [ent.path for ent in ctx.pane.entries if ent.is_dir]
    file_paths = [ent.path for ent in ctx.pane.entries if not ent.is_dir]

    is_all_dir_selected = len(dir_paths) != 0 and all(
        ent in selected_paths for ent in dir_paths
    )
    is_all_file_selected = len(file_paths) != 0 and all(
        ent in selected_paths for ent in file_paths
    )
    if is_all_dir_selected or is_all_file_selected:
        ctx.invoke("select_all")
        return

    _select_by_focus(ctx)


def select_by_extension(ctx) -> None:

    target = ctx.pane.selected() or ctx.pane.entries
    if not target:
        return

    exts = {item.suffix for item in target if item.suffix}
    if not exts:
        return

    focused = ctx.pane.focused.suffix
    exts = sorted(exts, key=lambda e: (e != focused, e))

    has_selections = 0 < len(ctx.pane.selected())

    def _select(i: int | None) -> None:
        if i is not None:
            if has_selections:
                ctx.pane.unselect(lambda ent: ent.suffix == exts[i])
            else:
                ctx.pane.select(lambda ent: ent.suffix == exts[i])

    title_prefix = "Select by" if not has_selections else "Unselect by"
    ctx.choose(title=f"{title_prefix} Extensions", items=exts, on_result=_select)


def fuzzy_selector(ctx) -> None:
    names = [e.name for e in ctx.pane.entries]
    selected = fzf_filter(ctx, names, multi=True)
    if 0 < len(selected):
        selected = set(selected)
        ctx.pane.select(lambda ent: ent.name in selected)

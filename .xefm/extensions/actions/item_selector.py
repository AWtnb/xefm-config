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

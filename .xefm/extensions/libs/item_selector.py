def select_under_cursor(ctx) -> None:
    ctx.pane.select(lambda ent: ent.path == ctx.pane.focused.path)


def select_only_files(ctx) -> None:
    ctx.pane.select(lambda ent: not ent.is_dir)


def select_only_dirs(ctx) -> None:
    ctx.pane.select(lambda ent: ent.is_dir)

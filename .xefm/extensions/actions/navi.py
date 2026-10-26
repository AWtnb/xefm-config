import os

DESKTOP_PATH = os.path.expanduser(r"~/Desktop")


def open_desktop(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)
    ctx.other.cd(DESKTOP_PATH)
    ctx.invoke("reset_pane_boundary")


def open_desktop_to_other(ctx) -> None:
    if DESKTOP_PATH not in [ctx.pane.path, ctx.other.path]:
        ctx.other.cd(DESKTOP_PATH)
    ctx.other.activate()

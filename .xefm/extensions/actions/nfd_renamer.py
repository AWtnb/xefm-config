import unicodedata

from ._utils import is_nfd


# https://github.com/crftwr/xefm/wiki/Spot-NFD-File-Names
def compose_nfd_names(ctx):
    """Rename the selected NFD names to their composed (NFC) spelling."""
    targets = [e for e in ctx.pane.selected() if is_nfd(e)]
    if not targets:
        ctx.message("No NFD names selected")
        return

    def rename(ok):
        if not ok:
            return
        # Where names are compared byte for byte (Linux), both spellings can be
        # two files side by side; renaming onto the other would replace it.
        on_disk = {e.path.name for e in ctx.pane.entries}
        for e in targets:
            composed = unicodedata.normalize("NFC", e.path.name)
            if composed in on_disk:
                ctx.message(f"{e.name}: an NFC file of that name already exists")
                continue
            try:
                e.path.rename(e.path.with_name(composed))
            except Exception as exc:  # noqa: BLE001
                ctx.message(f"{e.name}: {exc}")
        ctx.pane.refresh()

    ctx.confirm(f"Rename {len(targets)} name(s) to NFC?", on_result=rename)

import re
from pathlib import Path

REG_LR_PHOTO = re.compile(
    r"写真 ([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)( \([0-9]+\))?.jpg"
)


def _is_target(path: Path) -> bool:
    return REG_LR_PHOTO.fullmatch(path.name) is not None


def _pad2(s: str) -> str:
    return s.rjust(2, "0")


def _get_new_name(path: Path) -> str:
    m = REG_LR_PHOTO.fullmatch(path.name)
    assert m is not None
    yyyy = m.group(1)
    mm = _pad2(m.group(2))
    dd = _pad2(m.group(3))
    hh = _pad2(m.group(4))
    mi = _pad2(m.group(5))
    ss = _pad2(m.group(6))
    tail = m.group(7)
    suffix = "" if tail is None else f"-{tail.strip(' ()')}"
    return f"{yyyy}{mm}{dd}-IMG_{hh}{mi}{ss}{suffix}.jpg"


def rename_lightroom_photo(ctx) -> None:
    """
    Rename lightroom-processed photo file downloeded through dropbox
    """
    targets = [e for e in ctx.pane.selected() if _is_target(e.path)]
    if not targets:
        return

    def _rename(ok: bool) -> None:
        if not ok:
            return
        existing = {e.path.name for e in ctx.pane.entries}
        for ent in targets:
            new_name = _get_new_name(ent.path)
            if new_name in existing:
                ctx.message(f"{ent.name}: name already exists")
                continue
            try:
                ent.path.rename(ent.path.with_name(new_name))
                ctx.message(f"Renamed: {ent.name}")
                ctx.message(f"    ===> {new_name}")
            except Exception as e:  # noqa: BLE001
                ctx.message(f"{ent.name}: {e}")
        ctx.pane.refresh()

    ctx.confirm(f"Rename {len(targets)} item(s)?", on_result=_rename)

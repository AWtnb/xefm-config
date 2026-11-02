import datetime
import re
from pathlib import Path

from PIL import Image as PILImage  # ty: ignore[unresolved-import]
from PIL.ExifTags import TAGS  # ty: ignore[unresolved-import]

_REG_LR_PHOTO = re.compile(
    r"写真 ([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)( \([0-9]+\))?.jpg"
)


def _is_lightroom_photo(path: Path) -> bool:
    return _REG_LR_PHOTO.fullmatch(path.name) is not None


def _pad2(s: str) -> str:
    return s.rjust(2, "0")


def _get_new_name(path: Path) -> str:
    m = _REG_LR_PHOTO.fullmatch(path.name)
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
    targets = [e for e in ctx.pane.selected() if _is_lightroom_photo(e.path)]
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


_TZ_JST = datetime.timezone(datetime.timedelta(hours=9))


def _get_exif_timestamp(path: Path) -> datetime.datetime | None:
    try:
        with PILImage.open(path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return None
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTimeOriginal":
                    dt = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S").replace(
                        tzinfo=_TZ_JST
                    )
                    return dt
            return None
    except Exception as e:  # noqa: BLE001
        print(e)
        return None


def _timestamp_position_of(path: Path) -> int | None:
    name = path.name
    ext = path.suffix.lower().removeprefix(".")
    if ext in ["jpeg", "jpg", "webp"]:
        return None
    if ext == "raf":
        if name.startswith("_DSF"):
            return 0x19E
        return 0x17A
    if ext == "cr2":
        return 0x144
    if name.startswith("MVI_") and ext == "mp4":
        return 0x160
    return -1


def _get_timestamp(path: Path) -> datetime.datetime | None:

    offset = _timestamp_position_of(path)
    if offset is None:
        return _get_exif_timestamp(path)

    if offset < 1:
        return None

    with open(path, "rb") as f:
        f.seek(offset)
        bytes_read = f.read(19)
    decoded = bytes_read.decode("ascii")
    return datetime.datetime.strptime(decoded, "%Y:%m:%d %H:%M:%S").replace(
        tzinfo=_TZ_JST
    )


_TS_FORMAT = "%Y_%m%d_%H%M%S00"
_TS_FILLER = datetime.datetime.fromtimestamp(0, tz=_TZ_JST)


def rename_photo_by_exif_timestamp(ctx) -> None:
    """
    Rename photo files by its exif-based timestamp
    """

    targets = ctx.pane.selected()
    if not targets:
        return

    def _rename(ok: bool) -> None:
        if not ok:
            return
        existing = {e.path.name for e in ctx.pane.entries}
        for ent in targets:
            ts = _get_timestamp(ent.path)
            prefix = (
                _TS_FILLER.strftime(_TS_FORMAT)
                if ts is None
                else ts.strftime(_TS_FORMAT)
            )
            new_name = f"{prefix}_{ent.path.name}"
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

import unicodedata
from datetime import datetime

from xefm.user_api import Cell  # ty: ignore[unresolved-import]


def _is_nfd(entry):
    return not unicodedata.is_normalized("NFC", entry.path.name)


def _name_form(_, entries):
    return ["NFD" if _is_nfd(e) else None for e in entries]


def _nfd_mark(value, _):
    return Cell("NFD", color="orange") if value else ""


# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.md

ATTRIBUTES = {
    "name_form": {
        "label": "Name form",
        "type": "enum",
        "read": _name_form,
        "where": ["local", "archive", "ssh", "s3"],
        "values": {"NFD": {"label": "Name stored decomposed (NFD)", "color": "orange"}},
    },
}


def _smart_mtime(_, entry):
    mtime = entry.mtime
    if mtime is None:
        return ""

    dt = datetime.fromtimestamp(mtime)

    now = datetime.now()
    fmt = "%m-%d %H:%M:%S" if dt.year == now.year else "%Y-%m-%d %H:%M:%S"
    return dt.strftime(fmt)


LAYOUTS = {
    "smart-mtime": {
        "label": "Smart mtime",
        "columns": [
            {"attr": "name", "priority": 4},
            {"attr": "ext"},
            {"attr": "size", "priority": 1},
            {
                "attr": "mtime",
                "format": _smart_mtime,
                "align": "right",
                "width": len("yyyy-mm-dd hh:MM:ss"),
                "priority": 2,
            },
        ],
    },
}
DEFAULT_LAYOUT = "smart-mtime"

LAYOUT_EXTRAS = {
    "nfd": {
        "label": "NFD names",
        "markers": [
            {"attr": "name_form", "format": _nfd_mark, "on": "name", "side": "after"}
        ],
    },
}

import unicodedata

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
DEFAULT_LAYOUT = "default"

ATTRIBUTES = {
    "name_form": {
        "label": "Name form",
        "type": "enum",
        "read": _name_form,
        "where": ["local", "archive", "ssh", "s3"],
        "values": {"NFD": {"label": "Name stored decomposed (NFD)", "color": "orange"}},
    },
}

LAYOUTS = {}

LAYOUT_EXTRAS = {
    "nfd": {
        "label": "NFD names",
        "markers": [
            {"attr": "name_form", "format": _nfd_mark, "on": "name", "side": "after"}
        ],
    },
}

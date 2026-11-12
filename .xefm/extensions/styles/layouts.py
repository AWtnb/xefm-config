# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.md

import os
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

from xefm import favorites  # ty: ignore[unresolved-import]
from xefm.user_api import Cell  # ty: ignore[unresolved-import]


def smart_mtime(_, entry):
    mtime = entry.mtime
    if mtime is None:
        return ""

    dt = datetime.fromtimestamp(mtime)

    now = datetime.now()
    fmt = "%Y-%m-%d %H:%M:%S"
    if dt.year == now.year:
        fmt = (
            "%H:%M:%S"
            if dt.month == now.month and dt.day == now.day
            else "%m-%d %H:%M:%S"
        )
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
                "format": smart_mtime,
                "align": "right",
                "width": len("yyyy-mm-dd hh:MM:ss"),
                "priority": 2,
            },
        ],
    },
}
DEFAULT_LAYOUT = "smart-mtime"


def read_name_form(_, entries):
    return [
        "NFD" if not unicodedata.is_normalized("NFC", e.path.name) else None
        for e in entries
    ]


def _git_output(path, *args):
    try:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            check=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return result.stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def _is_under_git(path: str | Path) -> bool:
    current = Path(path).resolve()
    for p in (current, *current.parents):
        if (p / ".git").exists():
            return True
    return False


ATTENTION_SYMBOL = "!"


def read_git_status(directory, entries) -> list:
    if _is_under_git(directory):
        return [None for _ in entries]

    values = []

    for entry in entries:
        path = entry.path

        if not path.is_dir() or not (path / ".git").exists():
            values.append(None)
            continue

        status = _git_output(
            path, "status", "--porcelain", "--untracked-files=all", "--", "."
        )
        if status is None:
            values.append(None)
            continue

        ahead = _git_output(path, "rev-list", "--count", "@{upstream}..HEAD")
        has_unpushed = ahead is not None and ahead.strip().isdigit() and 0 < int(ahead)

        values.append(ATTENTION_SYMBOL if status.strip() or has_unpushed else None)

    return values


def _is_junction(p: Path):
    try:
        return bool(
            os.lstat(p).st_file_attributes & 0x400
        )  # FILE_ATTRIBUTE_REPARSE_POINT
    except (OSError, AttributeError):
        return False


def _is_link(path: Path) -> bool:
    return path.is_symlink() or _is_junction(path)


LINK_SYMBOL = "\u2197"


def read_link_dummy(_, entries) -> list:
    values = []
    for entry in entries:
        path = Path(entry.path)
        if _is_link(path):
            values.append(LINK_SYMBOL)
        else:
            values.append(None)

    return values


FAV_SYMBOL = "\u2605"


def read_favorites(_, entries) -> list:
    fav_paths = {f.path for f in favorites.get_favorites()}
    values = []
    for entry in entries:
        if str(entry.path) in fav_paths:
            values.append(FAV_SYMBOL)
        else:
            values.append(None)

    return values


ATTRIBUTES = {
    "name_form": {
        "label": "Name form",
        "type": "text",
        "read": read_name_form,
        "where": ["local", "archive", "ssh", "s3"],
    },
    "git_attention": {
        "label": "Git changes",
        "type": "text",
        "read": read_git_status,
        "where": "local",
    },
    "link_dummy": {
        "label": "Link dummies",
        "type": "text",
        "read": read_link_dummy,
        "where": "local",
    },
    "favorites": {
        "label": "Favorites",
        "type": "text",
        "read": read_favorites,
        "where": ["local", "archive", "ssh", "s3"],
    },
}


def nfd_marker(value, _):
    return Cell(value, color="orange") if value else ""


def git_attention_marker(value, _):
    return Cell(value, color="orange") if value else ""


def link_dummy_marker(value, _):
    return Cell(value, color="blue") if value else ""


def fav_marker(value, _):
    return Cell(value, color="purple") if value else ""


LAYOUT_EXTRAS = {
    "nfd": {
        "label": "NFD names",
        "markers": [
            {
                "attr": "name_form",
                "format": nfd_marker,
                "on": "name",
                "side": "after",
            }
        ],
    },
    "git_attention": {
        "label": "Git changes",
        "markers": [
            {
                "attr": "git_attention",
                "format": git_attention_marker,
                "on": "name",
                "side": "before",
            },
        ],
    },
    "link_dummy": {
        "label": "Link dummies",
        "markers": [
            {
                "attr": "link_dummy",
                "format": link_dummy_marker,
                "on": "name",
                "side": "after",
            },
        ],
    },
    "favorites": {
        "label": "Favorites",
        "markers": [
            {
                "attr": "favorites",
                "format": fav_marker,
                "on": "name",
                "side": "after",
            },
        ],
    },
}

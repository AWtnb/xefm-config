# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_LIST_LAYOUTS_FEATURE.md

import os
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

from xefm.user_api import Cell  # ty: ignore[unresolved-import]


def smart_mtime(_, entry):
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
                "format": smart_mtime,
                "align": "right",
                "width": len("yyyy-mm-dd hh:MM:ss"),
                "priority": 2,
            },
        ],
    },
}
DEFAULT_LAYOUT = "smart-mtime"


def name_form(_, entries):
    return [
        "NFD" if not unicodedata.is_normalized("NFC", e.path.name) else None
        for e in entries
    ]


def nfd_mark(value, _):
    return Cell("NFD", color="orange") if value else ""


def _git_output(path, *args):
    try:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            check=True,
            capture_output=True,
            text=True,
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


def git_attention(directory, entries) -> list:
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


def git_attention_marker(value, _):
    return Cell(ATTENTION_SYMBOL, color="orange") if value == ATTENTION_SYMBOL else ""


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


def link_dummy(_, entries) -> list:

    values = []
    for entry in entries:
        path = Path(entry.path)
        if _is_link(path):
            values.append(LINK_SYMBOL)
        else:
            values.append(None)

    return values


def link_dummy_marker(value, _):
    return Cell(LINK_SYMBOL, color="blue") if value == LINK_SYMBOL else ""


ATTRIBUTES = {
    "name_form": {
        "label": "Name form",
        "type": "enum",
        "read": name_form,
        "where": ["local", "archive", "ssh", "s3"],
        "values": {"NFD": {"label": "Name stored decomposed (NFD)", "color": "orange"}},
    },
    "git_attention": {
        "label": "Git changes",
        "type": "enum",
        "read": git_attention,
        "where": "local",
        "values": {
            ATTENTION_SYMBOL: {
                "label": "Uncommitted or unpushed changes",
                "color": "orange",
            },
        },
    },
    "link_dummy": {
        "label": "Link dummies",
        "type": "enum",
        "read": link_dummy,
        "where": "local",
        "values": {
            LINK_SYMBOL: {"label": "Link to other directory", "color": "blue"},
        },
    },
}


LAYOUT_EXTRAS = {
    "nfd": {
        "label": "NFD names",
        "markers": [
            {"attr": "name_form", "format": nfd_mark, "on": "name", "side": "after"}
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
}

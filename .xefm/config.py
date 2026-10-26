import os
import platform  # noqa: F401
import sys

import actions  # ty: ignore[unresolved-import]
import themes  # ty: ignore[unresolved-import]
from xefm.backend_detector import is_desktop_mode  # ty: ignore[unresolved-import]
from xefm.external_programs import (  # ty: ignore[unresolved-import]
    xefm_python,
    xefm_tool,
)


class Config:
    # ja: https://github.com/crftwr/xefm/blob/main/doc/CONFIGURATION_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CONFIGURATION_FEATURE.md
    UI_FONT_NAME = "HackGen" if sys.platform == "win32" else None
    MONO_FONT_NAME = "HackGen" if sys.platform == "win32" else None
    FONT_SIZE = 16

    SHOW_HIDDEN_FILES = True
    DEFAULT_LEFT_PANE_RATIO = 0.5
    DEFAULT_LOG_HEIGHT_RATIO = 0.25
    DATE_FORMAT = "full"
    DEFAULT_SORT_MODE = "name"
    DEFAULT_SORT_REVERSE = False
    THEMES = {"Phosphor": themes.phosphor_theme}  # noqa: RUF012

    # ja: https://github.com/crftwr/xefm/blob/main/doc/TRASH_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/TRASH_FEATURE.md
    DELETE_TO_TRASH = True

    # ja: https://github.com/crftwr/xefm/blob/main/doc/FILE_OPERATIONS_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/FILE_OPERATIONS_FEATURE.md
    CONFIRM_TRASH = True
    CONFIRM_DELETE = True
    CONFIRM_QUIT = True
    CONFIRM_COPY = True
    CONFIRM_MOVE = True
    CONFIRM_DUPLICATE = False
    CONFIRM_EXTRACT_ARCHIVE = True
    CONFIRM_ARCHIVE_CREATE = True

    # ja: https://github.com/crftwr/xefm/blob/main/doc/FILE_OPERATIONS_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/FILE_OPERATIONS_FEATURE.md
    TRANSFER_CONCURRENCY = "auto"
    FILE_OP_WORKERS_LOCAL = 4
    FILE_OP_WORKERS_S3 = 8

    DRIVE_LOCATIONS = None
    NETWORK_SERVERS = []  # noqa: RUF012

    MAX_LOG_MESSAGES = 1000
    MAX_HISTORY_ENTRIES = 100

    PROGRESS_ANIMATION_PATTERN = "spinner"
    PROGRESS_ANIMATION_SPEED = 0.2
    REDUCED_MOTION = False
    SEPARATE_EXTENSIONS = True
    MAX_EXTENSION_LENGTH = 5

    # ja: https://github.com/crftwr/xefm/blob/main/doc/MIGEMO_SEARCH_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/MIGEMO_SEARCH_FEATURE.md
    MIGEMO_SEARCH = False
    MIGEMO_MIN_LENGTH = 3
    MIGEMO_ROMAJI_TABLE = "default"

    # ja: https://github.com/crftwr/xefm/blob/main/doc/TEXT_EDITOR_FEATURE.ja.md
    # ja: https://github.com/crftwr/xefm/blob/main/doc/TEXT_ENCODING_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/TEXT_EDITOR_FEATURE.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/TEXT_ENCODING_FEATURE.md
    TEXT_EDITOR = "vim"
    TEXT_ENCODINGS = ["utf-8", "cp932", "euc-jp", "iso-2022-jp", "latin-1"]  # noqa: RUF012
    TEXT_DIFF = ["code", "--diff"] if is_desktop_mode() else "vimdiff"

    # ja: https://github.com/crftwr/xefm/blob/main/doc/EXTERNAL_TERMINAL_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/EXTERNAL_TERMINAL_FEATURE.md
    SUBSHELL = ["powershell", "-nop", "-nologo"]  # noqa: RUF012
    TERMINAL = None

    S3_CACHE_TTL = 60
    SSH_CACHE_TTL = 30
    SSH_CACHE_ERROR_TTL = 300

    ARCHIVE_CACHE_MAX_OPEN = 5
    ARCHIVE_CACHE_TTL = 300

    # ja: https://github.com/crftwr/xefm/blob/main/doc/FILE_MONITORING_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/FILE_MONITORING_FEATURE.md
    FILE_MONITORING_ENABLED = True
    FILE_MONITORING_COALESCE_DELAY_MS = 200
    FILE_MONITORING_MAX_RELOADS_PER_SECOND = 5
    FILE_MONITORING_FALLBACK_POLL_INTERVAL_S = 5

    # ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
    FAVORITES = [  # noqa: RUF012
        {"name": "Desktop", "path": os.path.expanduser(r"~/Desktop")},
        {"name": "Dropbox", "path": os.path.expanduser(r"~/Dropbox")},
        {"name": "AppData", "path": os.path.expanduser(r"~/AppData")},
    ]

    # ja: https://github.com/crftwr/xefm/blob/main/doc/FILE_ASSOCIATIONS_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/FILE_ASSOCIATIONS_FEATURE.md
    FILE_ASSOCIATIONS = [  # noqa: RUF012
        {
            "pattern": [
                "*.doc",
                "*.docx",
                "*.xls",
                "*.xlsx",
                "*.ppt",
                "*.pptx",
            ],
            "enter": "viewer",
            "open|edit": ["cmd", "/c", "start"],
        },
        {
            "pattern": ["*.md", "*.txt"],
            "edit": ["vim"],
        },
        {
            "pattern": ["*.jar", "*.whl", "*.egg"],
            "enter": "navigate",
        },
    ]

    # ja: https://github.com/crftwr/xefm/blob/main/doc/EXTERNAL_PROGRAMS_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/EXTERNAL_PROGRAMS_FEATURE.md
    PROGRAMS = [  # noqa: RUF012
        {"name": "Open in VSCode", "command": [xefm_python, xefm_tool("vscode.py")]},
    ]

    KEY_PRESET = None
    KEY_SEQUENCE_TIMEOUT = 1.0

    ACTIONS, EVENT_HOOKS, KEY_BINDINGS = actions.apply()

    def underscore_based_sortkey(entry) -> tuple:
        name = entry.name  # ty: ignore[unresolved-attribute]
        stem, ext = os.path.splitext(name)
        underscore_count = len(name) - len(name.lstrip("_"))

        return (
            not name.startswith("."),
            not name.startswith("_"),
            (-1 * underscore_count),
            stem.lower(),
            ext.lower(),
        )

    # ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
    # ja: https://github.com/crftwr/xefm/blob/main/doc/SORT_DIALOG_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/SORT_DIALOG_FEATURE.md
    SORT_KEYS = {  # noqa: RUF012
        "filename": {"key": underscore_based_sortkey, "override": True}
    }
    FILTERS = {}  # noqa: RUF012
    IMAGE_DECODERS = {}  # noqa: RUF012
    PATH_SCHEMES = {}  # noqa: RUF012
    MENU_ITEMS = {}  # noqa: RUF012
    LEXERS = {}  # noqa: RUF012

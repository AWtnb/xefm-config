"""
XeFM User Configuration

This file contains your personal XeFM configuration.
You can modify any of these settings to customize XeFM behavior.
"""

import importlib
import os
import platform  # noqa: F401
import sys
from types import ModuleType

# Import backend detector for runtime backend detection
from xefm.backend_detector import is_desktop_mode  # ty: ignore[unresolved-import]

# Import xefm_tool function and xefm_python variable for external program configuration
from xefm.external_programs import (  # ty: ignore[unresolved-import]
    xefm_python,
    xefm_tool,
)


def register_config_path(dir_name: str) -> None:
    user_profile = os.environ.get("USERPROFILE")
    assert user_profile is not None
    config_dir = os.path.join(user_profile, dir_name)
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)


register_config_path(".xefm")


def import_config(config_module_name: str) -> ModuleType:
    for name in list(sys.modules):
        if name == config_module_name or name.startswith(config_module_name + "."):
            del sys.modules[name]

    return importlib.import_module(config_module_name)


PREFERENCE = import_config("preference")


class Config:
    """User configuration for XeFM"""

    # --- Desktop (GUI) mode fonts (ignored in TUI mode) ----------------------
    # UI_FONT_NAME   : proportional default face (file names, labels,
    #                  dialogs, markdown prose).
    # MONO_FONT_NAME : monospaced face for aligned content (size/date
    #                  columns, viewer, diffs); also grounds the layout
    #                  grid, so it must be monospaced.
    # FONT_SIZE      : point size applied to BOTH faces.
    # Missing glyphs use the OS's native font substitution.
    #
    # None = the OS system default face -- already a matched pair per platform:
    #   macOS   -> San Francisco + SF Mono
    #   Windows -> Segoe UI + Consolas
    #
    # To use named fonts, uncomment ONE block below (it runs after the defaults
    # and overrides them). `sys` is already imported at the top of this file.

    UI_FONT_NAME = None
    MONO_FONT_NAME = None

    if sys.platform == "win32":
        UI_FONT_NAME = "Segoe UI"
        MONO_FONT_NAME = "Consolas"

    FONT_SIZE = 14  # point size for both faces (8-72)

    # Text viewer: the encodings offered by the viewer's encoding picker (the
    # 'change_encoding' action, Shift-E). Automatic detection — UTF-8 with or without
    # BOM, UTF-16/32 by BOM, Shift-JIS, EUC-JP, ISO-2022-JP, CP1252 — is built
    # in and always the default; this list only feeds the manual picker, for
    # when detection gets a file wrong. Any Python codec name works here
    # (e.g. 'koi8-r', 'gb2312', 'utf-16-le'):
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    TEXT_ENCODINGS = ["utf-8", "cp932", "euc-jp", "iso-2022-jp", "latin-1"]  # noqa: RUF012

    # Display settings
    SHOW_HIDDEN_FILES = True
    DEFAULT_LEFT_PANE_RATIO = 0.5  # 0.1 to 0.9
    DEFAULT_LOG_HEIGHT_RATIO = 0.25  # 0.1 to 0.5
    DATE_FORMAT = "full"  # 'short' (YY-MM-DD HH:mm) or 'full' (YYYY-MM-DD HH:mm:ss)

    # Sorting settings
    DEFAULT_SORT_MODE = "name"  # 'name', 'size', 'date'
    DEFAULT_SORT_REVERSE = False

    THEMES = PREFERENCE.THEMES

    # Behavior settings
    CONFIRM_DELETE = True  # Show confirmation dialog before deleting files/directories
    CONFIRM_QUIT = True  # Show confirmation dialog before quitting XeFM
    CONFIRM_COPY = True  # Show confirmation dialog before copying files/directories
    CONFIRM_MOVE = True  # Show confirmation dialog before moving files/directories
    CONFIRM_DUPLICATE = (
        True  # Show confirmation dialog before duplicating files/directories
    )
    CONFIRM_EXTRACT_ARCHIVE = (
        True  # Show confirmation dialog before extracting archives
    )
    CONFIRM_ARCHIVE_CREATE = True  # Show confirmation dialog before creating archives
    FILE_OP_WORKERS_LOCAL = 4  # Copy/move worker threads, local disk (1 = sequential)
    FILE_OP_WORKERS_S3 = (
        8  # Copy/move worker threads when S3 is involved (ssh is always 1)
    )

    KEY_BINDINGS = PREFERENCE.KEY_BINDINGS

    ACTIONS = PREFERENCE.ACTIONS

    EVENT_HOOKS = PREFERENCE.EVENT_HOOKS

    SORT_KEYS = PREFERENCE.SORT_KEYS

    FILTERS = PREFERENCE.FILTERS

    FAVORITE_DIRECTORIES = PREFERENCE.FAVORITE_DIRECTORIES

    # Drives dialog (D) - the fixed locations listed above everything the picker
    # discovers on its own (Windows drive letters, /Volumes, /media, /mnt, the
    # hosts in ~/.ssh/config, and your S3 buckets when AWS credentials are set).
    #
    # None = XeFM's built-in set: Home, Root (POSIX only), and whichever of
    # Documents / Downloads / Desktop exist in your home directory. Define a list
    # to replace that set entirely; [] removes the fixed rows and leaves the
    # picker showing only the discovered ones.
    #
    # Each entry needs 'name' and 'path'. A local path that does not exist is
    # skipped. A remote location (ssh:// s3://) is listed as written - nothing
    # connects until you select it.
    #
    # DRIVE_LOCATIONS = [
    #     {'name': 'Home', 'path': '~'},
    #     {'name': 'Work', 'path': '~/work'},
    #     {'name': 'NAS', 'path': 'ssh://nas/'},
    # ]
    DRIVE_LOCATIONS = None

    # Performance settings
    MAX_LOG_MESSAGES = 1000

    # History settings
    MAX_HISTORY_ENTRIES = 100  # Maximum number of history entries to keep

    # Progress animation settings
    PROGRESS_ANIMATION_PATTERN = "spinner"  # 'spinner', 'dots', 'progress', 'bounce', 'pulse', 'wave', 'clock', 'arrow'
    PROGRESS_ANIMATION_SPEED = 0.2  # Animation frame update interval in seconds

    # Motion settings
    # Suppress decorative motion app-wide: dialogs appear at once instead of
    # scaling in, and an animated theme background (Sci-Fi's starfield) coasts to
    # a stop and holds a still frame. Everything lands in its FINAL state, never
    # frozen mid-animation, so nothing is hidden by turning this on. Set it if
    # motion is uncomfortable, or over a slow SSH link where every animated frame
    # is a screen repaint. Functional updates (progress, file-list reloads,
    # search results) are unaffected.
    REDUCED_MOTION = False

    # File display settings
    SEPARATE_EXTENSIONS = True  # Show file extensions separately from basenames
    MAX_EXTENSION_LENGTH = 5  # Maximum extension length to show separately

    # Incremental search settings
    # Migemo expands romaji into the Japanese it could spell, so incremental
    # search (the file panes, the text/diff viewers, and the filter-list
    # dialogs — favorites, history, drives …) finds Japanese names without an
    # IME: typing "kensaku" also matches 検索. Plain matching always still
    # applies — Migemo only ever adds matches. Patterns with glob characters
    # (* ? [) keep exact fnmatch behavior, and patterns shorter than
    # MIGEMO_MIN_LENGTH skip Migemo (1-2 character queries are slow to expand
    # and barely one kana anyway). Needs the pymigemo package (installed with
    # XeFM); without it searches quietly stay plain.
    MIGEMO_SEARCH = (
        False  # Add Migemo (romaji -> Japanese) matches to incremental search
    )
    MIGEMO_MIN_LENGTH = 3  # Shortest pattern handed to Migemo
    MIGEMO_ROMAJI_TABLE = "default"  # 'default' or 'azik'

    # Text editor settings
    # Supports both string and list formats:
    # - String format: 'vim' (single command, no arguments)
    # - List format: ['code', '--wait'] (command with arguments)
    # Automatically set based on actual running backend mode:
    # - Terminal mode (curses): vim
    # - Desktop mode (coregraphics): code (VS Code)
    TEXT_EDITOR = "code"

    # Text diff tool settings
    # Tool invoked when pressing 'E' (edit_file) key in DiffViewer or DirectoryDiffViewer
    # Supports both string and list formats:
    # - String format: 'vimdiff' (single command, no arguments)
    # - List format: ['code', '--diff'] (command with arguments)
    # Automatically set based on actual running backend mode:
    # - Terminal mode (curses): vimdiff (string format example)
    # - Desktop mode (coregraphics): code --diff (list format example)
    TEXT_DIFF = ["code", "--diff"] if is_desktop_mode() else "vimdiff"

    # Subshell settings
    # Shell launched by the 'subshell' action (Shift-X), terminal mode only.
    # None: use $SHELL if set, otherwise the platform default
    # (%COMSPEC% / cmd.exe on Windows, /bin/sh elsewhere).
    # Supports both string and list formats:
    # - String format: 'zsh' (single command, no arguments)
    # - List format: ['powershell', '-NoLogo'] (command with arguments)
    SUBSHELL = ["powershell", "-nop"]  # noqa: RUF012

    # S3 settings
    S3_CACHE_TTL = 60  # S3 cache TTL in seconds (default: 60 seconds)

    # SSH/SFTP cache settings
    SSH_CACHE_TTL = (
        30  # SSH cache TTL in seconds for successful results (default: 30 seconds)
    )
    SSH_CACHE_ERROR_TTL = 300  # SSH cache TTL in seconds for cached errors (default: 300 seconds / 5 minutes)

    # Archive cache settings
    ARCHIVE_CACHE_MAX_OPEN = 5  # Maximum number of archives to keep open simultaneously
    ARCHIVE_CACHE_TTL = (
        300  # Archive cache TTL in seconds (default: 300 seconds / 5 minutes)
    )

    # File monitoring settings
    FILE_MONITORING_ENABLED = True  # Enable/disable automatic file list reloading
    FILE_MONITORING_COALESCE_DELAY_MS = 200  # Event coalescing window in milliseconds
    FILE_MONITORING_MAX_RELOADS_PER_SECOND = (
        5  # Maximum reloads per second (rate limiting)
    )
    FILE_MONITORING_FALLBACK_POLL_INTERVAL_S = (
        5  # Polling interval for fallback mode (seconds)
    )

    FILE_ASSOCIATIONS = PREFERENCE.FILE_ASSOCIATIONS

    # External programs - each item has "name", "command", and optional "options" fields
    # The "command" field is a list for safe subprocess execution
    # Relative paths in the first element are resolved relative to the XeFM root directory (where xefm/app.py is located)
    # Use xefm_tool('tool_name') to search for tools in:
    #   1. ~/.xefm/tools/ (user-specific tools, highest priority)
    #   2. {xefm/app.py directory}/tools/ (system tools, fallback)
    # ~/.xefm/tools/ is created on first launch with example_tool.py in it —
    # copy that file as the starting point for your own tools.
    # The "options" field is a dictionary with program-specific options:
    #   - terminal: if True, hand the terminal over to the program and wait for
    #     it to exit — for full-screen / interactive programs (vim, less, a
    #     REPL). If it exits with an error, XeFM waits for Enter so the output
    #     stays readable. Terminal mode only; desktop mode has no terminal to
    #     hand over and refuses the launch with an error in the log pane.
    #   - auto_return: deprecated and ignored — launches never block XeFM.
    PROGRAMS = [  # noqa: RUF012
        {
            "name": "Make Tree",
            "command": [xefm_python, xefm_tool("make_tree.py")],
        },
        {
            "name": "Summarize for LLM",
            "command": [xefm_python, xefm_tool("summarize.py")],
        },
        {
            "name": "Summarize by source",
            "command": [xefm_python, xefm_tool("summarize_by.py")],
        },
        {"name": "Open in VSCode", "command": [xefm_python, xefm_tool("vscode.py")]},
        # Add your own programs here:
        # {'name': 'My Custom Tool', 'command': [xefm_python, xefm_tool('my_custom_tool.py')]},
        # {'name': 'My Script (direct path)', 'command': [xefm_python, '/path/to/script.py']},
        # {'name': 'Quick Command', 'command': ['ls', '-la']},
        # Full-screen / interactive programs need the terminal handed over:
        {
            "name": "View with bat",
            "command": ["bat", "--paging=always"],
            "options": {"terminal": True},
        },
        # {'name': 'Python REPL', 'command': ['python3'], 'options': {'terminal': True}},
    ]

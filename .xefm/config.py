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
    FONT_SIZE = 14

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
    CONFIRM_DUPLICATE = True
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

    # ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
    ACTIONS = {  # noqa: RUF012
        "open_in_vscode": actions.misc.open_in_vscode,
        "open_desktop": actions.misc.open_desktop,
        "open_desktop_both": actions.misc.open_desktop_both,
        "jump_down": actions.cursor_jump.jump_down,
        "jump_up": actions.cursor_jump.jump_up,
        "make_tree": actions.tree.make_tree,
        "summarize_by": actions.tree.summarize_by,
        "quick_copy": actions.misc.quick_copy,
        "quick_move": actions.misc.quick_move,
        "focus_newest_item": actions.cursor_jump.focus_newest_item,
        "smart_select_all": actions.item_selector.smart_select_all,
        "open_ghq_repo": actions.favorites.open_ghq_repo,
        "fuzzy_favorites": actions.favorites.fuzzy_favorites,
    }

    # ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
    EVENT_HOOKS = {  # noqa: RUF012
        "quit": [actions.hook.backup_favorites_on_quit],
        "file_open": [actions.hook.on_enter],
    }

    # ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
    # ja: https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.ja.md
    # ja: https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.ja.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.md
    # en: https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.md
    KEY_PRESET = None
    KEY_SEQUENCE_TIMEOUT = 1.0
    KEY_BINDINGS = {  # noqa: RUF012
        "quit": ["Q"],
        "help": ["?"],
        "redraw": ["F5"],
        "command_palette": ["X"],
        "open_in_vscode": ["Ctrl-Shift-V"],
        "open_desktop": ["0"],
        "open_desktop_both": ["BACKSLASH"],
        "open_ghq_repo": ["G"],
        "focus_newest_item": ["Alt-N"],
        "jump_down": ["Alt-J"],
        "jump_up": ["Alt-K"],
        "next_tab": [],
        "prev_tab": [],
        "close_tab": [],
        "cursor_top": ["HOME", "A"],
        "cursor_bottom": ["END", "E"],
        "cursor_up": ["UP", "K"],
        "cursor_down": ["DOWN", "J"],
        "page_up": ["PAGE_UP"],
        "page_down": ["PAGE_DOWN"],
        "open_item": ["ENTER", "L", "RIGHT"],
        "open_with_os": ["Ctrl-ENTER", "Ctrl-Alt-O"],
        "reveal_in_os": ["Ctrl-Shift-E"],
        "go_parent": ["BACKSPACE", "H", "LEFT"],
        "switch_pane": ["TAB"],
        "nav_left": [],
        "nav_right": [],
        "toggle_select_down": ["SPACE"],
        "toggle_select_up": ["Shift-SPACE"],
        "select_range": ["Ctrl-Alt-SPACE"],
        "smart_select_all": ["Ctrl-A"],
        "toggle_select_files": [],
        "unselect_all": ["U"],
        "copy_names": ["Ctrl-Shift-C"],
        "copy_paths": ["Ctrl-Shift-P"],
        "clipboard_paste": ["Ctrl-V"],
        "quick_copy": ["C"],
        "quick_move": ["M"],
        "delete_files": {
            "keys": ["Ctrl-D"],
            "selection": "required",
        },
        "rename": ["N"],
        "create_file": ["T"],
        "create_directory": {
            "keys": ["Ctrl-Shift-N"],
            "selection": "none",
        },
        "view_file": [],
        "edit_file": ["Ctrl-E"],
        "file_details": ["I"],
        "diff_files": ["EQUAL"],
        "diff_directories": ["Shift-EQUAL"],
        "create_archive": {
            "keys": ["P"],
            "selection": "required",
        },
        "extract_archive": ["Ctrl-X"],
        "isearch": ["F"],
        "find_files": ["Shift-F"],
        "find_in_files": ["Shift-G"],
        "filter": [";"],
        "clear_filter": [":"],
        "sort": ["S"],
        "quick_sort_name": ["1"],
        "quick_sort_ext": ["2"],
        "quick_sort_size": ["3"],
        "quick_sort_date": ["4"],
        "add_favorite": ["Ctrl-B"],
        "favorites": ["B"],
        "find_by_tag": ["Shift-T"],
        "flat_view": [],
        "jump_to_path": ["Ctrl-O"],
        "history": ["Ctrl-Z"],
        "drives": ["D"],
        "sync_current_to_other": ["O"],
        "sync_other_to_current": ["Shift-O"],
        "compare_selection": [],
        "adjust_pane_left": ["["],
        "adjust_pane_right": ["]"],
        "reset_pane_boundary": ["-", "|"],
        "adjust_log_up": ["{", "Alt-Up"],
        "adjust_log_down": ["}", "Alt-Down"],
        "reset_log_height": ["_"],
        "scroll_log_up": ["Shift-K"],
        "scroll_log_down": ["Shift-J"],
        "scroll_log_page_up": [],
        "scroll_log_page_down": [],
        "toggle_wrap": ["Alt-Z"],
        "toggle_view_mode": ["M"],
        "change_encoding": ["Shift-E"],
        "text_viewer.scroll_down": ["J", "DOWN"],
        "text_viewer.scroll_up": ["K", "UP"],
        "text_viewer.page_down": ["L", "Right"],
        "text_viewer.page_up": ["H", "Left"],
        "text_viewer.scroll_top": ["A", "HOME"],
        "text_viewer.scroll_bottom": ["E", "END"],
        "text_viewer.edit_file": ["Ctrl-E"],
        "image_viewer.zoom_in": ["+", "="],
        "image_viewer.zoom_out": ["-", "_"],
        "image_viewer.zoom_reset": ["0"],
        "image_viewer.next": ["DOWN"],
        "image_viewer.prev": ["UP"],
        "image_viewer.pan_up": ["Shift-UP"],
        "image_viewer.pan_down": ["Shift-DOWN"],
        "image_viewer.pan_left": ["Shift-LEFT"],
        "image_viewer.pan_right": ["Shift-RIGHT"],
        "toggle_hidden": [".", "Shift-H"],
        "toggle_color_scheme": [],
        "view_options": ["Z"],
        "settings_menu": ["Shift-Z"],
        "programs": ["Alt-X"],
        "subshell": ["Shift-X"],
        "edit_config": [],
        "reload_config": ["Ctrl-R"],
    }

    def underscore_based_sortkey(entry):
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

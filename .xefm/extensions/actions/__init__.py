import json
from pathlib import Path

from xefm import favorites as xefm_favorites  # ty: ignore[unresolved-import]

from . import (
    clipboard,
    cursor_jumper,
    favorites,
    item_selector,
    misc,
    navi,
    nfd_renamer,
    photo_renamer,
    tree,
)
from ._utils import IMAGE_FILE_PATTERNS

# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
_ACTIONS = {
    "compose_nfd_names": nfd_renamer.compose_nfd_names,
    "conc_pdf": misc.conc_pdf,
    "diff_with_vscode": misc.diff_with_vscode,
    "diffinity": misc.diffinity,
    "edit_config": {"func": misc.launch_config_repo, "override": True},
    "focus_newest_item": cursor_jumper.focus_newest_item,
    "focus_older_item": cursor_jumper.focus_older_item,
    "fuzzy_favorites": favorites.fuzzy_favorites,
    "fuzzy_ghq": favorites.fuzzy_ghq,
    "fuzzy_selector": item_selector.fuzzy_selector,
    "go_git_root": navi.go_git_root,
    "git_init": misc.git_init,
    "jump_down": cursor_jumper.jump_down,
    "jump_up": cursor_jumper.jump_up,
    "lazygit": misc.lazygit,
    "eject_current_drive": navi.eject_current_drive,
    "open_desktop_both": navi.open_desktop_both,
    "open_desktop_to_new_tab": navi.open_desktop_to_new_tab,
    "open_desktop_to_other": navi.open_desktop_to_other,
    "open_desktop": navi.open_desktop,
    "open_git_remote": misc.open_git_remote,
    "open_in_vscode": misc.open_in_vscode,
    "open_parent_to_new_tab": navi.open_parent_to_new_tab,
    "open_parent_to_other": navi.open_parent_to_other,
    "open_to_other": navi.open_to_other,
    "open_with_smoothcsv": misc.open_with_smoothcsv,
    "quick_copy": misc.quick_copy,
    "quick_move": misc.quick_move,
    "recycle_bin": misc.launch_recycle_bin,
    "rename_photo_by_exif_timestamp": photo_renamer.rename_photo_by_exif_timestamp,
    "rename_rightloom_photo": photo_renamer.rename_lightroom_photo,
    "save_image_on_clipboard": clipboard.save_image_on_clipboard,
    "select_by_extension": item_selector.select_by_extension,
    "select_nfd_names": item_selector.select_nfd_names,
    "smart_copy": clipboard.smart_copy,
    "smart_enter": navi.smart_enter,
    "smart_mkdir": misc.smart_mkdir,
    "smart_select_all": item_selector.smart_select_all,
    "write_dir_tree": tree.write_dir_tree,
}

# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.md
_KEY_BINDINGS = {
    "add_favorite": ["Ctrl-B"],
    "adjust_log_down": ["}", "Alt-Down"],
    "adjust_log_up": ["{", "Alt-Up"],
    "adjust_pane_left": ["["],
    "adjust_pane_right": ["]"],
    "change_encoding": ["Shift-E"],
    "check_extension_updates": [],
    "clear_filter": [": *"],
    "clipboard_clear": [],
    "clipboard_copy": ["Y"],
    "clipboard_cut": ["Ctrl-X", "Shift-Y"],
    "clipboard_paste": ["Ctrl-V"],
    "close_tab": ["T W"],
    "command_palette": ["X"],
    "compare_selection": [],
    "connect_server": [],
    "context_menu": ["/", "F10", "APPS"],
    "context_menu_dir": ["?", "Shift-F10", "Shift-APPS"],
    "copy_files": [],
    "copy_files_to": {"keys": ["Shift-C"], "selection": "required"},
    "copy_log_all": [],
    "copy_log_selection": [],
    "copy_names": [],
    "copy_paths": [],
    "create_archive": {"keys": ["Shift-Z"], "selection": "required"},
    "create_directory": [],
    "create_file": ["N F"],
    "cursor_bottom": ["END", "E"],
    "cursor_down": ["DOWN", "J"],
    "cursor_next_selected": [],
    "cursor_prev_selected": [],
    "cursor_top": ["HOME", "A"],
    "cursor_up": ["UP", "K"],
    "delete_files": {"keys": ["Ctrl-D"], "selection": "required"},
    "delete_permanently": {
        "keys": ["Shift-DELETE"],
        "selection": "required",
    },
    "diff_directories": ["Shift-5"],
    "diff_files": ["5"],
    "drives": ["D"],
    "duplicate_files": ["Shift-D"],
    "edit_config": [],
    "edit_file": ["Ctrl-E"],
    "extensions": [],
    "extract_archive": ["Z"],
    "favorites": [],
    "fuzzy_favorites": ["B"],
    "fuzzy_ghq": ["G"],
    "fuzzy_selector": ["Shift-S"],
    "file_details": ["I"],
    "file_diff.scroll_bottom": ["E", "END"],
    "file_diff.scroll_down": ["J", "DOWN"],
    "file_diff.scroll_top": ["A", "HOME"],
    "file_diff.scroll_up": ["K", "UP"],
    "filter": [": :"],
    "find_by_tag": [],
    "find_files": ["Ctrl-F"],
    "find_in_files": [],
    "flat_view": ["Shift-B"],
    "focus_left": [],
    "focus_newest_item": ["Alt-N"],
    "focus_older_item": ["Alt-B"],
    "focus_right": [],
    "go_back": ["Alt-LEFT"],
    "go_forward": ["Alt-RIGHT"],
    "go_git_root": ["0 ^"],
    "go_parent": ["BACKSPACE", "H", "LEFT"],
    "go_root": [],
    "help": ["F1"],
    "history": ["Ctrl-Z"],
    "image_viewer.next": ["DOWN", "J"],
    "image_viewer.pan_down": ["Shift-DOWN"],
    "image_viewer.pan_left": ["Shift-LEFT"],
    "image_viewer.pan_right": ["Shift-RIGHT"],
    "image_viewer.pan_up": ["Shift-UP"],
    "image_viewer.prev": ["UP", "K"],
    "image_viewer.zoom_in": ["+", "="],
    "image_viewer.zoom_out": ["-", "_"],
    "image_viewer.zoom_reset": ["0"],
    "index_search": [],
    "install_extension": [],
    "isearch": ["F"],
    "jobs": [],
    "jump_down": ["Alt-J"],
    "jump_to_path": ["Ctrl-G"],
    "jump_up": ["Alt-K"],
    "menu": ["ALT"],
    "move_files": [],
    "move_files_to": {"keys": ["Shift-M"], "selection": "required"},
    "nav_left": [],
    "nav_right": [],
    "next_tab": ["T T"],
    "open_desktop": ["0 0"],
    "open_desktop_both": ["0 SPACE"],
    "open_desktop_to_other": ["0 O"],
    "open_desktop_to_new_tab": ["T 0"],
    "open_in_new_tab": ["T ENTER"],
    "open_in_vscode": ["Shift-V"],
    "open_list_from_command": ["Shift-F"],
    "open_list_from_clipboard": [],
    "open_item": [],
    "open_with_smoothcsv": [","],
    "open_parent_to_other": ["Shift-U"],
    "open_parent_to_new_tab": ["T U"],
    "open_with_os": ["Ctrl-ENTER", "Ctrl-O"],
    "open_to_other": ["Shift-L"],
    "page_down": ["PAGE_DOWN"],
    "page_up": ["PAGE_UP"],
    "prev_tab": ["T Shift-T"],
    "programs": ["Alt-X"],
    "quick_copy": ["C"],
    "quick_move": ["M"],
    "quick_sort_date": ["4"],
    "quick_sort_ext": ["2"],
    "quick_sort_name": ["1"],
    "quick_sort_size": ["3"],
    "quick_view": ["P"],
    "quit": ["Q"],
    "quit_app": [],
    "redraw": ["F5"],
    "reload_config": ["Ctrl-R"],
    "rename": ["N N"],
    "rename_in_editor": ["Shift-R"],
    "reset_log_height": ["_"],
    "reset_pane_boundary": ["MINUS", "|"],
    "reveal_in_os": ["Shift-E"],
    "save_image_on_clipboard": ["Shift-I"],
    "scroll_log_down": ["Shift-J", "Shift-DOWN"],
    "scroll_log_page_down": [],
    "scroll_log_page_up": [],
    "scroll_log_up": ["Shift-K", "Shift-UP"],
    "select_by_pattern": ["*"],
    "select_range": ["R"],
    "select_same_extension": [";"],
    "select_by_extension": ["Shift-X"],
    "settings_menu": ["Shift-Z"],
    "smart_copy": ["Ctrl-C"],
    "smart_enter": ["L", "RIGHT", "ENTER"],
    "smart_mkdir": ["N D"],
    "smart_select_all": ["Ctrl-A"],
    "sort": ["S"],
    "subshell": ["@"],
    "switch_pane": ["TAB"],
    "sync_current_to_other": ["O O"],
    "sync_other_to_current": ["O Shift-O"],
    "sync_python_packages": [],
    "text_viewer.edit_file": ["Ctrl-E"],
    "text_viewer.page_down": ["L", "Right"],
    "text_viewer.page_up": ["H", "Left"],
    "text_viewer.scroll_bottom": ["E", "END"],
    "text_viewer.scroll_down": ["J", "DOWN"],
    "text_viewer.scroll_top": ["A", "HOME"],
    "text_viewer.scroll_up": ["K", "UP"],
    "text_viewer.toggle_view_mode": ["M"],
    "toggle_color_scheme": ["F6"],
    "toggle_hidden": [".", "Shift-H"],
    "toggle_select_down": ["SPACE"],
    "toggle_select_files": [],
    "toggle_select_items": [],
    "toggle_select_up": ["Shift-SPACE"],
    "toggle_wrap": ["Alt-Z"],
    "unselect_all": ["U"],
    "unselect_by_pattern": [],
    "view_file": ["Shift-ENTER", "V"],
}


def reset_layout(ctx, _) -> None:
    ctx.invoke("reset_pane_boundary")
    ctx.invoke("reset_log_height")


def backup_favorites(ctx, _) -> bool:
    favs = xefm_favorites.get_favorites()  # list[FavoriteEntry]
    rows = [
        {"name": f.name, "path": f.path, "is_file": f.is_file, "origin": f.origin}
        for f in favs
    ]

    path = Path.home() / "xefm-favs-backup.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001
        ctx.message(f"Failed to backup favorites: {e}")

    return False


def close_quick_view(ctx, _) -> None:
    if ctx._app._quick_view:
        ctx._app._close_quick_view()


# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
_EVENT_HOOKS = {
    "startup": [reset_layout],
    "directory_changed": [close_quick_view],
    "quit": [backup_favorites],
}

# https://github.com/crftwr/xefm/blob/main/doc/FILE_ASSOCIATIONS_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/FILE_ASSOCIATIONS_FEATURE.md
# https://github.com/crftwr/xefm/blob/main/doc/OPEN_WITH_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/OPEN_WITH_FEATURE.md
_FILE_ASSOCIATIONS = [
    {
        "pattern": [
            "*.doc",
            "*.docx",
            "*.xls",
            "*.xlsx",
            "*.ppt",
            "*.pptx",
        ],
        "edit": None,
    },
    {
        "pattern": ["*"],
        "open_with": [
            {
                "name": "Mery",
                "command": [Path.home() / "AppData/Local/Programs/Mery/Mery.exe"],
            },
            {
                "name": "Notepad",
                "command": ["C:/Windows/System32/notepad.exe"],
            },
        ],
    },
    {
        "pattern": ["*.txt"],
        "open_with": [
            {
                "name": "Smooth CSV",
                "command": ["C:/Program Files/SmoothCSV/smoothcsv-cli.exe"],
            },
        ],
    },
    {
        "pattern": IMAGE_FILE_PATTERNS,
        "edit": None,
        "view": ["qimgv"],  # https://github.com/easymodo/qimgv
    },
    {
        "pattern": ["*.md"],
        "view": ["cmd", "/c", "start", "", "tinta"],  # https://tinta.cc/
    },
    {
        "pattern": ["*.csv"],
        "edit": {"action": "open_with_os"},
    },
    {
        "pattern": ["*.zip"],
        "open": {"action": "extract_archive"},
    },
    {
        "pattern": ["*.jar", "*.whl", "*.egg"],
        "enter": "navigate",
    },
]


def setup(text_editor: str | list[str]) -> tuple[dict | list, ...]:
    def _summarize(ctx) -> None:
        """
        summarize pane entries
        """
        tree.summarize(ctx, text_editor)

    actions = _ACTIONS | {"summarize": _summarize}
    return (actions, _EVENT_HOOKS, _KEY_BINDINGS, _FILE_ASSOCIATIONS)

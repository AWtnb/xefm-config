import json
import os

from xefm import favorites as xefm_favorites  # ty: ignore[unresolved-import]

from . import cursor_jump, favorites, item_selector, misc, tree

# ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
_ACTIONS = {
    "edit_config": {"func": misc.launch_config_repo, "override": True},
    "focus_newest_item": cursor_jump.focus_newest_item,
    "fuzzy_favorites": favorites.fuzzy_favorites,
    "jump_down": cursor_jump.jump_down,
    "jump_up": cursor_jump.jump_up,
    "make_tree": tree.make_tree,
    "open_desktop_both": misc.open_desktop_both,
    "open_desktop": misc.open_desktop,
    "open_ghq_repo": favorites.open_ghq_repo,
    "open_in_vscode": misc.open_in_vscode,
    "quick_copy": misc.quick_copy,
    "quick_move": misc.quick_move,
    "smart_select_all": item_selector.smart_select_all,
    "summarize_by": tree.summarize_by,
}

# ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# ja: https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.ja.md
# ja: https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.ja.md
# en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
# en: https://github.com/crftwr/xefm/blob/main/doc/KEY_BINDINGS_FEATURE.md
# en: https://github.com/crftwr/xefm/blob/main/doc/KEYMAP_PRESETS_FEATURE.md
_KEY_BINDINGS = {
    "add_favorite": ["Ctrl-B"],
    "adjust_log_down": ["}", "Alt-Down"],
    "adjust_log_up": ["{", "Alt-Up"],
    "adjust_pane_left": ["["],
    "adjust_pane_right": ["]"],
    "change_encoding": ["Shift-E"],
    "check_extension_updates": [],
    "clear_filter": [":"],
    "clipboard_clear": [],
    "clipboard_copy": ["Ctrl-C", "Y"],
    "clipboard_cut": ["Ctrl-X", "Shift-Y"],
    "clipboard_paste": ["Ctrl-V"],
    "close_tab": [],
    "command_palette": ["X"],
    "compare_selection": ["W"],
    "connect_server": [],
    "context_menu": ["/", "Shift-F10", "APPS"],
    "context_menu_dir": ["?", "Alt-Shift-F10", "Shift-APPS"],
    "copy_files": [],
    "copy_files_to": {"keys": ["Shift-C"], "selection": "required"},
    "copy_log_all": [],
    "copy_log_selection": [],
    "copy_names": ["Ctrl-N"],
    "copy_paths": ["Ctrl-P"],
    "create_archive": {"keys": ["P"], "selection": "required"},
    "create_directory": {"keys": ["Ctrl-Shift-N"], "selection": "none"},
    "create_file": ["T"],
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
    "edit_config": {"keys": ["Ctrl-E"], "selection": "none"},
    "edit_file": {"keys": ["Ctrl-E"], "selection": "required"},
    "extensions": [],
    "extract_archive": ["Shift-P"],
    "favorites": ["B"],
    "file_details": ["I"],
    "file_diff.scroll_bottom": ["E", "END"],
    "file_diff.scroll_down": ["J", "DOWN"],
    "file_diff.scroll_top": ["A", "HOME"],
    "file_diff.scroll_up": ["K", "UP"],
    "filter": [";"],
    "find_by_tag": ["Shift-T"],
    "find_files": ["Shift-F"],
    "find_in_files": ["Shift-G"],
    "flat_view": ["Shift-B"],
    "focus_left": [],
    "focus_newest_item": ["Alt-N"],
    "focus_right": [],
    "go_back": ["Alt-LEFT"],
    "go_forward": ["Alt-RIGHT"],
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
    "index_search": ["Ctrl-F"],
    "install_extension": [],
    "isearch": ["F"],
    "jobs": ["Ctrl-G"],
    "jump_down": ["Alt-J"],
    "jump_to_path": ["Ctrl-J"],
    "jump_up": ["Alt-K"],
    "menu": ["F10", "ALT"],
    "move_files": [],
    "move_files_to": {"keys": ["Shift-M"], "selection": "required"},
    "nav_left": [],
    "nav_right": [],
    "next_tab": [],
    "open_desktop": ["0"],
    "open_desktop_both": ["BACKSLASH"],
    "open_ghq_repo": ["G"],
    "open_in_new_tab": [],
    "open_in_vscode": ["Ctrl-Shift-V"],
    "open_item": ["ENTER", "L", "RIGHT"],
    "open_with_os": ["Ctrl-ENTER", "Ctrl-O"],
    "page_down": ["PAGE_DOWN"],
    "page_up": ["PAGE_UP"],
    "prev_tab": [],
    "programs": ["Alt-X"],
    "quick_copy": ["C"],
    "quick_move": ["M"],
    "quick_sort_date": ["4"],
    "quick_sort_ext": ["2"],
    "quick_sort_name": ["1"],
    "quick_sort_size": ["3"],
    "quick_view": ["Shift-V"],
    "quit": ["Q"],
    "quit_app": [],
    "redraw": ["F5"],
    "reload_config": ["Ctrl-R"],
    "rename": ["N"],
    "rename_in_editor": ["Shift-R"],
    "reset_log_height": ["_"],
    "reset_pane_boundary": ["MINUS", "|"],
    "reveal_in_os": ["Ctrl-Shift-E"],
    "scroll_log_down": ["Shift-J", "Shift-DOWN"],
    "scroll_log_page_down": [],
    "scroll_log_page_up": [],
    "scroll_log_up": ["Shift-K", "Shift-UP"],
    "select_by_pattern": ["+", "*"],
    "select_range": ["Ctrl-Alt-SPACE"],
    "select_same_extension": [],
    "settings_menu": ["Shift-Z"],
    "smart_select_all": ["Ctrl-A"],
    "sort": ["S"],
    "subshell": ["Shift-X"],
    "switch_pane": ["TAB"],
    "sync_current_to_other": ["O"],
    "sync_other_to_current": ["Shift-O"],
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
    "view_file": ["V"],
    "view_options": ["Z"],
}


def validate_keys(ctx, _) -> None:
    counts = {}
    for k, v in _KEY_BINDINGS.items():
        if "." in k:
            continue
        keys = v if isinstance(v, list) else v["keys"]
        for key in keys:
            counts[key] = counts.get(key, 0) + 1

    for key, count in sorted(counts.items()):
        if 1 < count:
            ctx.message(f"[WARNING] Key duplicates: {key} ({count} times)")


def on_enter(ctx, event) -> bool:
    if event.path.suffix.lower() in [".pdf", ".tbx", ".cmx"]:
        ctx.invoke("open_with_os")
        return True
    return False


def backup_favorites_on_quit(ctx, _) -> bool:

    favs = xefm_favorites.get_favorites()  # list[FavoriteEntry]
    rows = [
        {"name": f.name, "path": f.path, "is_file": f.is_file, "origin": f.origin}
        for f in favs
    ]

    path = os.path.expanduser("~/xefm-favs-backup.json")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001
        ctx.message(f"Failed to backup favorites: {e}")

    return False


# ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
_EVENT_HOOKS = {
    "startup": [validate_keys],
    "quit": [backup_favorites_on_quit],
    "file_open": [on_enter],
}


def apply() -> tuple[dict, dict, dict]:
    return (_ACTIONS, _EVENT_HOOKS, _KEY_BINDINGS)

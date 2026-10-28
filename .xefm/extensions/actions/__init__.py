import json
import os

from xefm import favorites as xefm_favorites  # ty: ignore[unresolved-import]

from . import clipboard, cursor_jumper, favorites, item_selector, misc, navi, tree

# ja: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.ja.md
# en: https://github.com/crftwr/xefm/blob/main/doc/CUSTOMIZATION_FEATURE.md
_ACTIONS = {
    "edit_config": {"func": misc.launch_config_repo, "override": True},
    "conc_pdf": misc.conc_pdf,
    "focus_newest_item": cursor_jumper.focus_newest_item,
    "focus_older_item": cursor_jumper.focus_older_item,
    "fuzzy_favorites": favorites.fuzzy_favorites,
    "jump_down": cursor_jumper.jump_down,
    "jump_up": cursor_jumper.jump_up,
    "make_tree": tree.make_tree,
    "recycle_bin": misc.launch_recycle_bin,
    "open_desktop_both": navi.open_desktop_both,
    "open_desktop_to_other": navi.open_desktop_to_other,
    "open_desktop": navi.open_desktop,
    "open_parent_to_other": navi.open_parent_to_other,
    "open_ghq_repo": favorites.open_ghq_repo,
    "open_in_smoothcsv": misc.open_in_smoothcsv,
    "open_in_vscode": misc.open_in_vscode,
    "open_to_other": navi.open_to_other,
    "quick_copy": misc.quick_copy,
    "quick_move": misc.quick_move,
    "select_by_extension": item_selector.select_by_extension,
    "smart_copy": clipboard.smart_copy,
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
    "clear_filter": [": *"],
    "clipboard_clear": [],
    "clipboard_copy": ["Y"],
    "clipboard_cut": ["Ctrl-X", "Shift-Y"],
    "clipboard_paste": ["Ctrl-V"],
    "close_tab": [],
    "command_palette": ["X"],
    "compare_selection": ["W"],
    "connect_server": [],
    "context_menu": ["/", "F10", "APPS"],
    "context_menu_dir": ["?", "Shift-F10", "Shift-APPS"],
    "copy_files": [],
    "copy_files_to": {"keys": ["Shift-C"], "selection": "required"},
    "copy_log_all": [],
    "copy_log_selection": [],
    "copy_names": ["Ctrl-N"],
    "copy_paths": ["Ctrl-P"],
    "create_archive": {"keys": ["Shift-P", "Shift-Z"], "selection": "required"},
    "create_directory": {"keys": ["D", "Shift-N"], "selection": "none"},
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
    "duplicate_files": ["Shift-D"],
    "edit_config": ["Ctrl-E Ctrl-E"],
    "edit_file": ["Ctrl-E Ctrl-ENTER"],
    "extensions": [],
    "extract_archive": ["P", "Z"],
    "favorites": ["B"],
    "file_details": ["I"],
    "file_diff.scroll_bottom": ["E", "END"],
    "file_diff.scroll_down": ["J", "DOWN"],
    "file_diff.scroll_top": ["A", "HOME"],
    "file_diff.scroll_up": ["K", "UP"],
    "filter": [": :"],
    "find_by_tag": ["Shift-T"],
    "find_files": ["Shift-F"],
    "find_in_files": ["Shift-G", "Ctrl-Shift-F"],
    "flat_view": ["Shift-B"],
    "focus_left": [],
    "focus_newest_item": ["Alt-N"],
    "focus_older_item": ["Alt-B"],
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
    "jobs": [],
    "jump_down": ["Alt-J"],
    "jump_to_path": ["Ctrl-G", "Ctrl-Shift-O"],
    "jump_up": ["Alt-K"],
    "menu": ["ALT"],
    "move_files": [],
    "move_files_to": {"keys": ["Shift-M"], "selection": "required"},
    "nav_left": [],
    "nav_right": [],
    "next_tab": [],
    "open_desktop": ["0 0"],
    "open_desktop_both": ["BACKSLASH", "0 SPACE"],
    "open_desktop_to_other": ["0 O"],
    "open_ghq_repo": ["G"],
    "open_in_new_tab": [],
    "open_in_smoothcsv": [","],
    "open_in_vscode": ["Ctrl-Shift-V"],
    "open_item": ["ENTER", "L", "RIGHT"],
    "open_parent_to_other": ["Shift-U"],
    "open_with_os": ["Ctrl-ENTER", "Ctrl-O"],
    "open_to_other": ["Shift-L"],
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
    "rename": ["N", "F2"],
    "rename_in_editor": ["Shift-R"],
    "reset_log_height": ["_"],
    "reset_pane_boundary": ["MINUS", "|"],
    "reveal_in_os": ["Ctrl-Shift-E"],
    "scroll_log_down": ["Shift-J", "Shift-DOWN"],
    "scroll_log_page_down": [],
    "scroll_log_page_up": [],
    "scroll_log_up": ["Shift-K", "Shift-UP"],
    "select_by_pattern": ["*"],
    "select_range": ["Ctrl-Alt-SPACE"],
    "select_same_extension": [";"],
    "select_by_extension": ["Shift-X"],
    "settings_menu": ["Shift-Z"],
    "smart_copy": ["Ctrl-C"],
    "smart_select_all": ["Ctrl-A"],
    "sort": ["S"],
    "subshell": ["@"],
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
}


def validate_keys(ctx, _) -> None:
    counts = {}
    for k, v in _KEY_BINDINGS.items():
        if "." in k:
            continue
        keys = (
            v
            if isinstance(v, list)
            else [f"{s}(selection: {v['selection']})" for s in v["keys"]]
        )
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


def setup() -> tuple[dict, dict, dict]:
    return (_ACTIONS, _EVENT_HOOKS, _KEY_BINDINGS)

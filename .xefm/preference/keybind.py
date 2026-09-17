# Key bindings - customize your shortcuts
# Each action can have multiple keys assigned to it
#
# Supported formats:
# 1. Simple format: 'action': ['key1', 'key2']
#    - Works regardless of selection status
#    - Keys can be characters ('a', 'Q') or special key names ('HOME', 'END')
#
# 2. Extended format: 'action': {'keys': ['key1', 'key2'], 'selection': 'any|required|none'}
#    - 'any': works regardless of selection status (default)
#    - 'required': only works when at least one item is explicitly selected
#    - 'none': only works when no items are explicitly selected
#
# Special key names (use these strings in the keys list):
#   'HOME', 'END', 'PPAGE', 'NPAGE', 'UP', 'DOWN',
#   'LEFT', 'RIGHT', 'BACKSPACE', 'DELETE', 'INSERT',
#   'F1' through 'F12'

bindings = {
    # === Application Control ===
    "quit": ["Q"],  # Exit XeFM application
    "help": ["?"],  # Show help dialog with all key bindings
    "redraw": ["F5"],  # Additional redraw trigger (Ctrl-L is always hardcoded)
    #
    # === Navigation ===
    "cursor_up": ["UP", "K"],  # Move cursor up one item
    "cursor_down": ["DOWN", "J"],  # Move cursor down one item
    "page_up": ["PAGE_UP"],  # Move cursor up one page
    "page_down": ["PAGE_DOWN"],  # Move cursor down one page
    "open_item": ["ENTER", "L", "RIGHT"],  # Open file/directory or enter directory
    "open_with_os": ["Ctrl-ENTER"],  # Open file(s) with OS default application
    "reveal_in_os": ["Ctrl-Shift-E"],  # Reveal focused file in OS file manager
    "go_parent": ["BACKSPACE", "H", "LEFT"],  # Go to parent directory
    "switch_pane": ["TAB"],  # Switch between left and right panes
    "nav_left": [],  # Left pane: go to parent, Right pane: switch to left pane
    "nav_right": [],  # Right pane: go to parent, Left pane: switch to right pane
    #
    # === File Selection ===
    "toggle_select_down": ["SPACE"],  # Toggle selection of current file
    "toggle_select_up": ["Shift-SPACE"],  # Toggle selection and move up
    "toggle_select_files": ["Ctrl-A"],  # Select all items
    "unselect_all": ["U"],  # Unselect all items
    "select_all_files": ["Alt-F"],  # Toggle selection of all files in current pane
    "toggle_select_items": [],  # Toggle selection of all items (files + dirs)
    #
    # === Clipboard (copy names/paths to the system clipboard) ===
    "copy_names": ["Ctrl-Shift-C"],  # Copy selected/focused file name(s) to clipboard
    "copy_paths": ["Ctrl-Shift-P"],  # Copy selected/focused full path(s) to clipboard
    #
    # === File Operations ===
    "copy_files": {
        "keys": ["C"],
        "selection": "required",
    },  # Copy selected files to other pane
    "move_files": {
        "keys": ["M"],
        "selection": "required",
    },  # Move selected files to other pane
    "delete_files": {
        "keys": ["Ctrl-D"],
        "selection": "required",
    },  # Delete selected files/directories
    "rename": ["N"],  # Rename selected file/directory
    "create_file": ["T"],  # Create new file (prompts for filename)
    "create_directory": {
        "keys": ["Ctrl-Shift-N"],
        "selection": "none",
    },  # Create new directory (only when no files selected)
    #
    # === File Viewing & Editing ===
    "view_file": ["Shift-Enter"],  # View file using configured viewer
    "edit_file": [],  # Edit selected file with configured text editor
    "file_details": ["I"],  # Show detailed file information dialog
    #
    # === File Comparison ===
    "diff_files": ["EQUAL"],  # Compare two selected files side-by-side
    "diff_directories": ["Shift-EQUAL"],  # Compare directories recursively
    #
    # === Archive Operations ===
    "create_archive": {
        "keys": ["P"],
        "selection": "required",
    },  # Create archive from selected files
    "extract_archive": ["Ctrl-X"],  # Extract selected archive file
    #
    # === Search & Filter ===
    "isearch": ["F"],  # Enter incremental search mode (isearch)
    "find_files": ["Shift-F"],  # Show filename search dialog
    "find_in_files": ["Shift-G"],  # Show content search dialog (grep)
    "filter": [";"],  # Enter filter mode to show only matching files
    "clear_filter": [":"],  # Clear current file filter
    #
    # === Sorting ===
    "sort": ["S"],  # Open the sort dialog (key + order)
    "quick_sort_name": ["1"],  # Quick sort by filename
    "quick_sort_ext": ["2"],  # Quick sort by file extension
    "quick_sort_size": ["3"],  # Quick sort by file size
    "quick_sort_date": ["4"],  # Quick sort by modification date
    #
    # === Directory Navigation ===
    "favorites": ["Shift-B"],  # Show favorite directories dialog
    "jump_to_path": ["Ctrl-O"],  # Jump to path
    "history": ["Ctrl-Z"],  # Show history for current pane
    "drives": ["D"],  # Show drives/volumes dialog
    #
    # === Pane Management ===
    "sync_current_to_other": ["O"],  # Sync current pane directory to other pane
    "sync_other_to_current": [
        "Shift-O",
        "W",
    ],  # Sync other pane directory to current pane
    "compare_selection": [],  # Show file and directory comparison options
    "adjust_pane_left": ["["],  # Make left pane smaller (move boundary left)
    "adjust_pane_right": ["]"],  # Make left pane larger (move boundary right)
    "reset_pane_boundary": ["-", "|"],  # Reset pane split to 50% | 50%
    #
    # === Log Pane Control ===
    "adjust_log_up": ["{"],  # Make log pane larger (Shift+[)
    "adjust_log_down": ["}"],  # Make log pane smaller (Shift+])
    "reset_log_height": ["_"],  # Reset log pane height to default (Shift+-)
    "scroll_log_up": ["Shift-K"],  # Scroll log pane up one line
    "scroll_log_down": ["Shift-J"],  # Scroll log pane down one line
    "scroll_log_page_up": [],  # Scroll log pane up one page (to older messages)
    "scroll_log_page_down": [],  # Scroll log pane down one page (to newer messages)
    #
    # === Text Viewer ===
    # Text-viewer-only actions. 'isearch' (F, above) opens incremental search
    # inside the viewers too. These deliberately share keys with file-list
    # actions -- 'W' with 'compare_selection', 'M' with 'move_files' /
    # 'create_directory', 'Shift-E' with 'create_file'. The two surfaces never
    # apply at once, and each only ever looks at its own context's actions, so
    # a shared key is never ambiguous. Plain 'E' (edit_file, under File
    # Operations) works inside the text viewer too, editing the viewed file.
    "toggle_wrap": ["W"],  # Toggle line wrapping
    "toggle_view_mode": ["M"],  # Toggle rendered (Markdown) / raw text
    "change_encoding": ["Shift-E"],  # Choose the text encoding (auto / explicit)
    #
    # === Image Viewer ===
    # Image-viewer-only actions, scoped like the text viewer's above. '-' and
    # '_' intentionally share with
    # 'reset_pane_boundary' / 'reset_log_height', and the arrow /
    # Shift-arrow keys with the file list's cursor and log-scroll actions:
    # all of those apply to the file list only, never to an open viewer,
    # and each context matches its own action by name via
    # KeyBindings.is_action_for_event, so the shared keys are unambiguous.
    # Home/End jump to the first/last image and stay viewer-local (not
    # rebindable), like the text viewer's scroll keys.
    "image_viewer.zoom_in": [
        "+",
        "=",
    ],  # Image viewer: zoom in ('=' is unshifted '+')
    "image_viewer.zoom_out": ["-", "_"],  # Image viewer: zoom out
    "image_viewer.zoom_reset": ["0"],  # Image viewer: fit the whole image to the window
    "image_viewer.next": ["DOWN"],  # Image viewer: next image in the file list
    "image_viewer.prev": ["UP"],  # Image viewer: previous image in the file list
    "image_viewer.pan_up": ["Shift-UP"],  # Image viewer: pan up (while zoomed in)
    "image_viewer.pan_down": ["Shift-DOWN"],  # Image viewer: pan down
    "image_viewer.pan_left": ["Shift-LEFT"],  # Image viewer: pan left
    "image_viewer.pan_right": ["Shift-RIGHT"],  # Image viewer: pan right
    #
    # === Display & Appearance ===
    "toggle_hidden": [".", "Shift-H"],  # Toggle visibility of hidden files (dotfiles)
    # Unbound by default (use View → Theme in the menu bar). Assign a key
    # here to cycle themes from the keyboard, e.g. ['T'].
    "toggle_color_scheme": ["Shift-T"],  # Cycle to the next color theme
    "view_options": ["Z"],  # Show view options menu
    "settings_menu": ["Shift-Z"],  # Show settings and configuration menu
    #
    # === External Programs ===
    "programs": ["X"],  # Show external programs menu
    "subshell": ["Shift-X"],  # Enter subshell (command line) mode
    #
    # === Configuration ===
    # Unbound by default (reachable via the Tools menu). Assign a key here to
    # open/reload this file without leaving XeFM, e.g. 'edit_config': ['Y'].
    "edit_config": [],  # Edit this config.py in TEXT_EDITOR, then reload
    "reload_config": ["Ctrl-R"],  # Re-read this config.py and apply live
    #
    # === Viewer-local actions (rebindable, not listed above) ==============
    # Every key the modal viewers use is a named action too, and every one of
    # them can be rebound here. They are *not* listed as entries above,
    # because they already work without one: an action XeFM does not find in
    # this dictionary falls back to the default it declares in xefm/actions.py
    # (which is also what keeps a config written before an action existed
    # working). Add an entry only for the ones you want to change.
    #
    # The names are prefixed with the viewer they belong to, so they never
    # collide with the file list's own actions — and because each surface only
    # ever looks at its own names, a viewer action may share a key with a file
    # list action with no ambiguity at all. Their defaults:
    #
    #   Text viewer                        File diff
    #     'text_viewer.scroll_up':  UP       'file_diff.scroll_up':      UP
    #     'text_viewer.scroll_down': DOWN    'file_diff.scroll_down':    DOWN
    #     'text_viewer.page_up':    PAGE_UP  'file_diff.page_up':        PAGE_UP
    #     'text_viewer.page_down':  PAGE_DOWN 'file_diff.page_down':     PAGE_DOWN
    #     'text_viewer.scroll_top': HOME     'file_diff.scroll_top':     HOME
    #     'text_viewer.scroll_bottom': END   'file_diff.scroll_bottom':  END
    #     'text_viewer.scroll_left': LEFT    'file_diff.scroll_left':    LEFT
    #     'text_viewer.scroll_right': RIGHT  'file_diff.scroll_right':   RIGHT
    #                                        'file_diff.next_block':     n
    #   Image viewer                         'file_diff.prev_block':     Shift-N
    #     'image_viewer.first':     HOME
    #     'image_viewer.last':      END
    #
    #   Directory diff
    #     'dir_diff.cursor_up':   UP        'dir_diff.expand':      RIGHT
    #     'dir_diff.cursor_down': DOWN      'dir_diff.collapse':    LEFT
    #     'dir_diff.page_up':     PAGE_UP   'dir_diff.activate':    ENTER
    #     'dir_diff.page_down':   PAGE_DOWN 'dir_diff.switch_side': TAB
    #     'dir_diff.cursor_top':  HOME      'dir_diff.next_change': n
    #     'dir_diff.cursor_bottom': END     'dir_diff.prev_change': Shift-N
    #     'dir_diff.rescan':      r         'dir_diff.split_left':  [
    #                                       'dir_diff.split_right': ]
    #
    # Example -- page with space and b inside the text viewer only:
    # 'text_viewer.page_down': ['SPACE'],
    # 'text_viewer.page_up': ['B'],
    #
    # The same prefix also scopes a *shared* action to one viewer. 'quit',
    # 'help', 'isearch' and 'edit_file' are understood everywhere, so rebinding
    # 'quit' above changes it in the file list and in every viewer; writing
    # 'file_diff.quit' changes it in the file diff viewer alone:
    # 'file_diff.quit': ['X'],
}

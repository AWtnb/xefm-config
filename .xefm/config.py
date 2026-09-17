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
    SHOW_HIDDEN_FILES = False
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

    # -----------------------------------------------------------------------
    # In-process customization -- PREVIEW
    # -----------------------------------------------------------------------
    # This config file is executed Python, so it can define functions as well as
    # settings. ACTIONS binds your own functions to action names (which
    # KEY_BINDINGS above then binds to keys, exactly like a built-in action), and
    # EVENT_HOOKS runs them at set moments in XeFM's life.
    #
    # PREVIEW: this is not a stable API yet. The objects passed to your functions
    # and the shape of these two variables may change in any release until
    # xefm.user_api.API_VERSION reaches 1. XeFM logs one line saying so when a
    # config uses either variable. Everything else in this file is unaffected.
    #
    # Both reload with the rest of the config ('reload_config'), so iterating on
    # an action is edit-then-reload -- no restart.
    #
    # --- ACTIONS ----------------------------------------------------------
    # A function takes one argument, the context object, and is run on the UI
    # thread while XeFM waits -- so keep it quick. Anything it raises is logged
    # with a traceback and dropped; it never takes XeFM down.
    #
    # Define the functions ABOVE `class Config:` (module level), then:
    #
    # def select_documents(ctx):
    #     """Select every Word/PDF document in the active pane."""
    #     n = ctx.pane.select(lambda e: e.suffix.lower() in ('.docx', '.pdf'))
    #     ctx.message(f"Selected {n} document(s)")
    #
    # def go_to_sibling(ctx):
    #     """Point the other pane at this pane's directory."""
    #     ctx.other.cd(ctx.pane.path)
    #
    # ACTIONS = {
    #     'select-documents': select_documents,
    #     'go-to-sibling': go_to_sibling,
    # }
    # ...and bind them in KEY_BINDINGS above, like any built-in action:
    #     'select-documents': ['Shift-D'],
    #
    # An action name that already exists is ignored unless you say you meant it,
    # which also keeps the built-in reachable so you can wrap it:
    #
    # def confirm_then_quit(ctx):
    #     ctx.message("see you")
    #     ctx.invoke('quit')          # runs the built-in 'quit'
    #
    # ACTIONS = {'quit': {'func': confirm_then_quit, 'override': True}}
    #
    # What the context object offers:
    #   ctx.pane / ctx.other / ctx.left / ctx.right   the panes
    #   ctx.invoke(name)                              run another action
    #   ctx.message(text)                             one line in the log pane
    #   ctx.input(prompt, default, on_accept=fn)      ask for text
    #   ctx.choose(title, items, on_result=fn)        pick from a list
    #   ctx.confirm(prompt, on_result=fn)             yes / no
    # ...and on each pane:
    #   pane.path, pane.entries, pane.cursor, pane.focused, pane.selected()
    #   pane.select(predicate) / pane.unselect(predicate) / pane.refresh()
    #   pane.cd(path, focus_name=None)
    # Each entry has .name, .path, .suffix, .stem, .is_dir, .is_file, .is_link,
    # .size and .mtime.
    #
    # XeFM never blocks on a dialog, so input/choose/confirm hand their answer to
    # a callback instead of returning it -- put the rest of the action in there.
    ACTIONS = {}  # noqa: RUF012

    # --- EVENT_HOOKS ------------------------------------------------------
    # Functions run at set moments. Each event maps to a list, run in order.
    #
    #   'startup'           fn(ctx)            once the app is up
    #   'quit'              fn(ctx)            before XeFM shuts down
    #   'directory_changed' fn(ctx, pane, old_path, new_path)
    #   'file_open'         fn(ctx, path)      return True to claim the open
    #
    # 'file_open' fires before XeFM decides what to do with a file, so returning
    # True is how you route one file type somewhere of your own without touching
    # FILE_ASSOCIATIONS. It does not fire for directories -- entering one is
    # navigation, not opening.
    #
    # def log_visit(ctx, pane, old_path, new_path):
    #     with open(Path.home() / '.xefm' / 'visited.log', 'a') as f:
    #         f.write(f"{new_path}\n")
    #
    # def open_psd_in_gimp(ctx, path):
    #     if path.suffix.lower() != '.psd':
    #         return False
    #     subprocess.Popen(['gimp', str(path)])
    #     return True                 # claimed -- XeFM does nothing further
    #
    # EVENT_HOOKS = {
    #     'directory_changed': [log_visit],
    #     'file_open': [open_psd_in_gimp],
    # }
    EVENT_HOOKS = {}  # noqa: RUF012

    # --- SORT_KEYS --------------------------------------------------------
    # Your own sort orders. Each one becomes a row in the sort dialog ('s') and
    # in the Sort By menu, alongside Filename / Extension / Size / Timestamp.
    #
    # A sort key takes one entry and returns anything that can be compared --
    # XeFM sorts by whatever comes back. Return a tuple for a multi-level order;
    # tuples compare item by item, so (e.size, e.name) means "by size, and by
    # name within the same size".
    #
    # def size_then_name(entry):
    #     return (entry.size, entry.name)
    #
    # SORT_KEYS = {
    #     'biggest': {'label': 'Size, then name', 'key': size_then_name},
    # }
    #
    # Two things you do NOT have to handle: directories always come first, and
    # ascending/descending is applied for you. Your key only decides the order
    # inside one group. Reading entry.size or entry.mtime is free -- XeFM already
    # collected them for the listing.
    #
    # Naming one of the four built-in sorts -- 'filename', 'extension', 'size',
    # 'timestamp', the dialog's own rows in lower case -- replaces it, which
    # needs 'override': True so a typo cannot quietly change what Filename means. XeFM orders names by character code, which is not how
    # Explorer or Finder order a directory; this is where you change that:
    #
    # import locale, re                       # at the top of this file
    # locale.setlocale(locale.LC_COLLATE, '')  # your system's own ordering
    #
    # def by_system_order(entry):
    #     # digit runs as numbers, everything else through the system's ordering
    #     parts = re.split(r'(\d+)', entry.name)
    #     return [int(p) if i % 2 else locale.strxfrm(p) for i, p in enumerate(parts)]
    #
    # SORT_KEYS = {'filename': {'key': by_system_order, 'override': True}}
    #
    # That follows your locale, which is close to but not the same as the shell's
    # own order. Matching Explorer or Finder exactly means their comparison
    # functions -- StrCmpLogicalW and localizedStandardCompare: -- which compare
    # two names rather than producing a key, so wrap one in
    # functools.cmp_to_key(...) and expect it to cost more on a large directory.
    #
    # The rest of an entry: 'label' is the row text (defaults to the name),
    # 'explain' is the example line the dialog shows under the order, and
    # 'hotkey' is a letter that applies the sort straight from the dialog (a new
    # row gets its label's initial when no other row has claimed it).
    #
    # A key runs on a background thread, so keep it to arithmetic and strings.
    # One that fails, or returns things that cannot be compared with each other,
    # loses the sort rather than the listing: the pane falls back to ordering by
    # filename and says so once in the log pane.
    SORT_KEYS = {}  # noqa: RUF012

    # --- FILTERS ----------------------------------------------------------
    # Your own filters. Each one becomes a fixed row in the Filter dialog (';'),
    # under "clear filter" and above the patterns you have typed there before.
    #
    # The simple kind is one or more wildcard patterns:
    #
    # FILTERS = {
    #     'images': ['*.jpg', '*.jpeg', '*.png', '*.gif'],   # any one matches
    # }
    #
    # The other kind is a function, which is how you filter by something the
    # name does not say -- size, date, whatever you can work out from the entry.
    # It takes one entry and returns True to show it:
    #
    # import time                              # at the top of this file
    #
    # def modified_today(entry):
    #     return entry.mtime >= time.time() - 24 * 3600
    #
    # FILTERS = {
    #     'today': {'label': 'Modified today', 'match': modified_today},
    #     'big': {'label': 'Over 100 MB', 'match': lambda e: e.size > 100 << 20},
    # }
    #
    # 'label' is the row text and defaults to the name you gave it. An entry has
    # the same fields a sort key sees -- .name, .path, .suffix, .stem, .is_dir,
    # .is_file, .is_link, .size and .mtime -- and reading .size or .mtime is free.
    #
    # Directories are always shown, exactly as they are under a typed pattern: a
    # filter that hid them would take away the folder you were about to open. So
    # your function only decides which files are visible -- and "directories
    # only" is written 'match': lambda e: False.
    #
    # A name may not contain * ? or [ -- XeFM remembers a filter by its name and
    # a typed pattern as itself, and one that read as both could not be told
    # apart. Put the wildcards in 'pattern' and give the filter a plain name.
    #
    # Like a sort key, a filter function runs on a background thread, so keep it
    # to arithmetic and strings. One that fails loses the filter rather than the
    # listing: the pane shows everything and says so once in the log pane --
    # deliberately that way round, so a broken filter never hides files from an
    # operation you are about to run.
    FILTERS = {}  # noqa: RUF012

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
    TEXT_EDITOR = "code" if is_desktop_mode() else "vim"

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
    SUBSHELL = None

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

    # File extension associations
    # Maps file patterns to what each action should do.
    #
    # There are two tiers of "open", and they are bound to different keys:
    #
    #   'enter'  ENTER          Casual open. Stays inside XeFM. The value names
    #                           a built-in handler, NOT a program to launch:
    #                             'viewer'   - the built-in text/markdown viewer
    #                             'navigate' - browse the file as an archive
    #                                          (handy for *.jar, *.whl, ...)
    #                             None       - do nothing
    #                           With no rule, XeFM's default applies: directories
    #                           and archives are entered, files open in the
    #                           built-in viewer.
    #
    #   'open'   Cmd/Ctrl-ENTER Deliberate open. Hands the file to an external
    #                           program. Falls back to the OS default app.
    #
    # The other two actions are 'view' (V) and 'edit' (E), both external.
    #
    # Compact Format Features:
    # 1. Multiple patterns in one entry: ['*.jpg', '*.jpeg', '*.png']
    # 2. Combined actions: 'open|view' assigns same command to both actions
    # 3. Commands: List ['open', '-a', 'Preview'] or string 'open -a Preview'
    # 4. None: Action not available -- except 'view': None, which selects the
    #    built-in viewer, and 'enter': None, which does nothing.
    #
    # You do NOT declare whether a program takes over the terminal. That follows
    # from the backend, not from the program: in terminal mode XeFM suspends and
    # waits for the child (correct for less/vim; a launcher like `open -a` just
    # returns straight away), and in desktop mode there is no terminal to hand
    # over, so the child is detached and XeFM stays responsive. As with
    # TEXT_EDITOR above, pick programs that suit the mode you run in.
    #
    # Format:
    # {
    #     'pattern': '*.pdf' or ['*.jpg', '*.png'],  # Single or multiple fnmatch patterns
    #     'enter': 'viewer',         # Built-in handler for the ENTER key
    #     'open|view': ['command'],  # Same command for open and view
    #     'edit': ['command'],       # Different command for edit
    # }
    FILE_ASSOCIATIONS = [  # noqa: RUF012
        # PDF files
        {
            "pattern": "*.pdf",
            "open|view": ["cmd.exe", "/c", "start"],
            "edit": None,
        },
        # Image files. 'view' is deliberately None so V opens XeFM's own image
        # viewer (zoom / pan / prev-next, staying inside XeFM) rather than handing
        # the file to Preview; 'open' still hands it to the OS app for editing or
        # a full-fidelity look. Set 'open|view' back to Preview if you would
        # rather V left XeFM. Formats beyond these four still reach the built-in
        # viewer by falling through with no rule at all.
        {
            "pattern": ["*.jpg", "*.jpeg", "*.png", "*.gif"],
            "open": ["open", "-a", "Preview"],
            "view": None,
            "edit": ["open", "-a", "GIMP"],
        },
        # Video files
        {
            "pattern": ["*.mp4", "*.mov"],
            "open|view": ["open", "-a", "QuickTime Player"],
            "edit": None,
        },
        # Audio files
        {
            "pattern": ["*.mp3", "*.wav"],
            "open": ["open", "-a", "Music"],
            "edit": None,
        },
        # Microsoft Word documents
        {
            "pattern": ["*.doc", "*.docx"],
            "open|view|edit": ["open", "-a", "Microsoft Word"],
        },
        # Microsoft Excel spreadsheets
        {
            "pattern": ["*.xls", "*.xlsx"],
            "open|view|edit": ["open", "-a", "Microsoft Excel"],
        },
        # Microsoft PowerPoint presentations
        {
            "pattern": ["*.ppt", "*.pptx"],
            "open|view|edit": ["open", "-a", "Microsoft PowerPoint"],
        },
        # Note there is deliberately no entry listing text/code extensions.
        # Enter and V already fall through to the built-in viewer when no rule
        # matches, and the viewer sniffs the bytes -- so it reads text with no
        # configuration and shows a placeholder for binaries, including for
        # files with no extension or an unknown one that a list would miss.
        #
        # Zip-shaped archives XeFM does not enter by extension. This one *is*
        # worth stating, because it cannot be sniffed: .docx and .xlsx are zip
        # files too, and you want Word for those, not a file listing.
        {
            "pattern": ["*.jar", "*.whl", "*.egg"],
            "enter": "navigate",
        },
        # Add your own file associations here:
        # {
        #     'pattern': ['*.ext1', '*.ext2'],
        #     'enter': 'viewer',                  # what ENTER does (in XeFM)
        #     'open|view': ['command', 'args'],   # external programs
        #     'edit': ['command', 'args'],
        # },
        # Terminal programs need no special marking -- in terminal mode XeFM
        # hands the display over and waits:
        # {
        #     'pattern': '*.log',
        #     'view': ['less'],
        # },
    ]

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

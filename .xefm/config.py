"""
XeFM User Configuration

This file contains your personal XeFM configuration.
You can modify any of these settings to customize XeFM behavior.
"""

import os
import platform  # noqa: F401
import sys

import actions  # ty: ignore[unresolved-import]
import event_hooks  # ty: ignore[unresolved-import]
import keybindings  # ty: ignore[unresolved-import]
import themes  # ty: ignore[unresolved-import]

# Import backend detector for runtime backend detection
from xefm.backend_detector import is_desktop_mode  # ty: ignore[unresolved-import]

# Import xefm_tool function and xefm_python variable for external program configuration
from xefm.external_programs import (  # ty: ignore[unresolved-import]
    xefm_python,
    xefm_tool,
)


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

    THEMES = {"Phosphor": themes.phosphor_theme}  # noqa: RUF012

    # Behavior settings
    CONFIRM_TRASH = True
    CONFIRM_DELETE = True  # Show confirmation dialog before deleting files/directories

    # Delete key (delete_files): True sends local files to the system's Trash
    # (Recycle Bin on Windows) where their drive has one, and deletes for good
    # only where there is none (remote, archives, USB/network drives on
    # Windows) -- saying so first. False makes it delete permanently, as
    # delete_permanently always does.
    DELETE_TO_TRASH = True

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

    # How many files a copy, move or extraction may have in flight. "auto"
    # takes the number from the storage at each end — a local disk or mounted
    # volume four, S3 eight, ssh and archives one — "none" runs everything
    # sequentially, and an integer overrides the lot (an endpoint that allows
    # only one transfer still caps it at one). Closing a file is serialised
    # whatever this says: where the destination defers a file's transfer to its
    # close, that is the transfer, and one at a time is what a server was seen
    # to require.
    TRANSFER_CONCURRENCY = "auto"

    # Keymap preset: the whole keymap, chosen at first launch and changed from
    # Tools > Keymap. The presets are peers; neither is the default.
    #   None        -- whatever you chose at first launch or in Tools > Keymap
    #   'afx'       -- letters: C copy, K delete, M move ... The single-key
    #                  style of the X68000 filers and AFX (あふ). 'default' is
    #                  accepted as an old name for it.
    #   'orthodox'  -- function keys: F3 view, F4 edit, F5 copy, F6 move,
    #                  F7 new folder, F8 delete. No bare letter runs anything;
    #                  typing a letter starts incremental search.
    # Setting this wins over the Tools > Keymap menu. KEY_BINDINGS below is
    # laid over whichever preset is in force. See doc/KEYMAP_PRESETS_FEATURE.md.
    KEY_PRESET = None

    FILE_OP_WORKERS_LOCAL = 4  # Copy/move worker threads, local disk (1 = sequential)
    FILE_OP_WORKERS_S3 = (
        8  # Copy/move worker threads when S3 is involved (ssh is always 1)
    )

    KEY_BINDINGS = keybindings.bindings

    # -----------------------------------------------------------------------
    # In-process customization -- PREVIEW
    # -----------------------------------------------------------------------
    # This config file is executed Python, so it can define functions as well as
    # settings. ACTIONS binds your own functions to action names (which
    # KEY_BINDINGS above then binds to keys, exactly like a built-in action),
    # EVENT_HOOKS runs them at set moments in XeFM's life, SORT_KEYS lets you
    # write the order the file list is sorted in, FILTERS lets you write what
    # it shows, IMAGE_DECODERS lets you add picture formats the image viewer
    # does not read yet, PATH_SCHEMES lets you add a browsable folder that
    # is not a folder, and LEXERS lets you color a language the text viewer
    # does not know.
    #
    # PREVIEW: this is not a stable API yet. The objects passed to your functions
    # and the shape of these seven variables may change in any release until
    # xefm.user_api.API_VERSION reaches 1. XeFM logs one line saying so when a
    # config uses either variable. Everything else in this file is unaffected.
    #
    # Both reload with the rest of the config ('reload_config'), so iterating on
    # an action is edit-then-reload -- no restart.
    ACTIONS = actions.actions
    EVENT_HOOKS = event_hooks.event_hooks

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

    SORT_KEYS = {  # noqa: RUF012
        "filename": {"key": underscore_based_sortkey, "override": True}
    }

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

    # --- IMAGE_DECODERS ---------------------------------------------------
    # Picture formats the built-in image viewer does not read yet.
    #
    # It already reads a lot without help, and which formats depends on your
    # machine rather than on XeFM: on macOS it draws HEIC, JPEG XL and camera
    # RAW through the system's own decoder; on Windows through whichever WIC
    # codecs are installed (the HEIF and AV1 extensions from the Store, if you
    # have them); in a terminal through Pillow, including any Pillow plugin you
    # installed. Installing pillow-heif is enough to add HEIC anywhere:
    #
    #     pip install pillow-heif
    #
    # What is left after all that is the formats only a library XeFM does not
    # ship can read. Write a function that turns the file's bytes into a
    # picture, and name the suffix it is for:
    #
    #     import io                             # at the top of this file
    #
    #     def open_svg(data):
    #         import cairosvg
    #         from PIL import Image
    #         return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=data)))
    #
    #     def open_raw(data):
    #         import rawpy
    #         from PIL import Image
    #         with rawpy.imread(io.BytesIO(data)) as raw:
    #             return Image.fromarray(raw.postprocess())
    #
    #     IMAGE_DECODERS = {
    #         '.svg': open_svg,
    #         '.dng': open_raw,
    #         '.cr2': open_raw,
    #     }
    #
    # Your function gets the file's bytes -- not a path -- so the same decoder
    # works on a picture inside a zip or on an S3 bucket, with nothing copied to
    # a temp file first. Return a PIL.Image (the usual answer), or None for "I
    # cannot read this one".
    #
    # Registering a suffix is also what makes the viewer OFFER that format:
    # Enter on a .dng opens the picture rather than the binary viewer. XeFM only
    # ever claims formats something on the machine can actually decode, so it
    # never opens onto an "I cannot show this" card.
    #
    # Registering a suffix XeFM already reads replaces its decoder with yours --
    # that is how you override how a format is read, and it is the only way.
    #
    # Like a sort key or a filter, a decoder may run on a background thread, so
    # it must not touch the UI. One that fails costs that picture and nothing
    # else: the viewer shows the reason on its card and the log pane gets the
    # traceback.
    IMAGE_DECODERS = {}  # noqa: RUF012
    # --- PATH_SCHEMES -----------------------------------------------------
    # Your own browsable locations. A scheme like 'reg' makes 'reg://...' a
    # place XeFM can open in a pane, jump to (Shift-J), and keep in FAVORITE_
    # DIRECTORIES -- listed by your class rather than read off a disk.
    #
    # Inherit ReadOnlyPathImpl and write five methods. Everything else -- the
    # path arithmetic, refusing writes, what the pane and the status bar show --
    # comes with it.
    #
    # Define the class ABOVE `class Config:` (module level), with anything it
    # reads. Inside the class body it would *load* fine and then fail on every
    # call: a class body is not a scope the methods defined in it can see, so
    # NOTES and io below would come back as NameError the first time XeFM asked
    # the folder a question.
    #
    #     import io
    #     from xefm.path_base import ReadOnlyPathImpl, UriStatResult
    #
    #     NOTES = {'': ['todo', 'ideas'], 'todo': [], 'ideas': []}
    #
    #     class NotesPathImpl(ReadOnlyPathImpl):
    #         def exists(self):   return self._key in NOTES
    #         def is_dir(self):   return self._key in NOTES
    #         def iterdir(self):
    #             for name in NOTES.get(self._key, []):
    #                 yield self._child(name)
    #         def stat(self):     return UriStatResult(is_dir=self.is_dir())
    #         def open(self, mode='r', buffering=-1, encoding=None,
    #                  errors=None, newline=None):
    #             return io.StringIO('')
    #
    #     class Config:
    #         ...
    #
    # Then name it here -- this line, in the class, is the only part that
    # belongs at this indentation:
    #
    #     PATH_SCHEMES = {'notes': NotesPathImpl}
    #
    # self._key is the part after 'notes://', with no leading or trailing
    # slash -- '' at the root, 'todo/monday' further in. self._child(name)
    # builds a child; XeFM works out parents, names and suffixes itself.
    #
    # Writing is refused for you, with a clear message. Say why in your own
    # words with READ_ONLY_MESSAGE = 'edit these in the Notes app'.
    #
    # A class that is missing one of the five methods, or whose scheme name is
    # not a valid one, is skipped with a line in the log pane -- the rest of
    # your config still loads. A method that *raises* is reported the same way,
    # with its traceback, when something asks the folder a question.
    # See doc/VIRTUAL_FOLDERS_FEATURE.md.
    PATH_SCHEMES = {}  # noqa: RUF012

    # --- MENU_ITEMS -------------------------------------------------------
    # Put an action in a menu: the File menu ('file') and/or the menu a row
    # opens with a right-click or the Menu key ('context'). The key is the
    # action's name -- one of your ACTIONS, or a built-in one:
    #
    #     MENU_ITEMS = {
    #         'select-docs': {
    #             'menus': ['context'],
    #             'label': 'Select Documents',
    #             'when': 'entry',      # optional
    #         },
    #     }
    #
    # 'when' greys the item out unless it applies: 'entry' needs an entry under
    # the cursor, 'selection' needs at least one selected; the default is
    # 'always'. Your items gather in a group of their own near the foot of
    # each menu, in the order written here.
    MENU_ITEMS = {}  # noqa: RUF012

    # --- LEXERS -----------------------------------------------------------
    # Syntax highlighting for files the text viewer shows as plain text, or
    # colors as the wrong language. The coloring comes from Pygments, which
    # knows hundreds of languages; this names the lexer for a file name.
    #
    # The key is a file-name pattern ('*.mnl', or just '.mnl'; 'Jenkinsfile'
    # for a name with no suffix). The value is either the name of a lexer
    # Pygments already has -- `pygmentize -L lexers` lists them -- or a lexer
    # class of your own:
    #
    #     from autocad_lexers import DclLexer   # at the top of this file
    #
    #     LEXERS = {
    #         '*.dcl': DclLexer,      # your own lexer
    #         '*.mnl': 'newlisp',     # an existing one, for another suffix
    #     }
    #
    # Your own lexer is an ordinary Pygments lexer -- a RegexLexer subclass,
    # written the way https://pygments.org/docs/lexerdevelopment/ describes,
    # with nothing from XeFM in it. Keep it in its own file in
    # ~/.xefm/extensions/ (autocad_lexers.py above) and import it here. Its
    # own `filenames` attribute is not used: the key here alone decides which
    # files it colors. Its `aliases` are -- once registered, its alias can be
    # a value here too ('*.dclx': 'dcl').
    #
    # An entry here wins over Pygments' own choice for the same files, which
    # is how you recolor a suffix Pygments gives to another language. An
    # entry naming a lexer that does not exist is skipped with a line in the
    # log pane.

    LEXERS = {}  # noqa: RUF012

    FAVORITES = [  # noqa: RUF012
        {"name": "Desktop", "path": os.path.expanduser(r"~/Desktop")},
        {"name": "Dropbox", "path": os.path.expanduser(r"~/Dropbox")},
        {"name": "AppData", "path": os.path.expanduser(r"~/AppData")},
    ]

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

    # Connect to Server (Shift-D) - network servers you connect to often.
    # macOS and Windows only; on Linux the dialog is not offered.
    #
    # These are listed above the servers you save from the dialog itself, and
    # cannot be removed with Shift-Delete (this file is where they live, so
    # delete them here). Nothing is contacted until you pick a row.
    #
    # Each entry needs 'url'; 'name' labels the row (the URL is used when it is
    # missing) and 'user' prefills the account.
    #
    # NEVER put a password here. There is no field for one, and XeFM will not
    # read one. Tick "Save password" in the connection form instead - it goes
    # into the login keychain (macOS) or Credential Manager (Windows).
    #
    # NETWORK_SERVERS = [
    #     {'name': 'NAS Photo',  'url': 'smb://nas/photo', 'user': 'me'},
    #     {'name': 'NAS Backup', 'url': 'smb://nas/backup'},
    #     {'name': 'Docs',       'url': 'https://dav.example.com/files'},
    # ]
    NETWORK_SERVERS = []  # noqa: RUF012

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
    TEXT_EDITOR = "vim"

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

    # Terminal application (desktop mode only)
    # Desktop mode has no terminal of its own to hand over, so the subshell and
    # PROGRAMS entries with {'terminal': True} open in this application instead.
    # TERMINAL decides the window; SUBSHELL decides the shell inside it. The
    # command to run is appended as trailing arguments.
    # None: the platform default -- Terminal.app on macOS; Windows Terminal
    # (wt.exe) on Windows if installed, otherwise a new console window.
    # Supports both string and list formats:
    # - ['open', '-a', 'iTerm']      (macOS: any app that runs a script it opens)
    # - ['wezterm', 'start', '--']   (a terminal that takes the command as args)
    TERMINAL = None

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

    FILE_ASSOCIATIONS = [  # noqa: RUF012
        # Microsoft Office
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
        {"name": "Open in VSCode", "command": [xefm_python, xefm_tool("vscode.py")]},
        # Add your own programs here:
        # {'name': 'My Custom Tool', 'command': [xefm_python, xefm_tool('my_custom_tool.py')]},
        # {'name': 'My Script (direct path)', 'command': [xefm_python, '/path/to/script.py']},
        # {'name': 'Quick Command', 'command': ['ls', '-la']},
        # Full-screen / interactive programs need the terminal handed over:
        # {'name': 'Python REPL', 'command': ['python3'], 'options': {'terminal': True}},
    ]

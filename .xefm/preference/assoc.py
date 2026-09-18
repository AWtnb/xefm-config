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

file_associations = [
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

# -----------------------------------------------------------------------
# Custom themes (optional)
# -----------------------------------------------------------------------
# Register your own named themes here. Each one is added to the theme picker
# (View > Theme) and the T-key cycle alongside the built-ins — Dark+, Monokai,
# Dracula, Nord, Solarized, Gruvbox Dark, Light+, Solarized Light — so you can
# switch between them at run time. XeFM starts on Dark+ and remembers whichever
# theme you last switched to across restarts.
#
# THEMES maps a display name to a dict of color overrides. A theme inherits a
# base and overrides only what differs: set 'base' to any built-in (or another
# theme you defined above) to inherit it; with no 'base' it builds on the theme
# of the same name if one exists (so {'Dark+': {...}} tweaks the built-in), else
# on 'Dark+'. A name matching an existing theme replaces it in place.
#
# Every available key (all optional). Colors are (R, G, B) tuples, 0-255:
#
#   'base':          'Dark+'          # theme to inherit (see above for default)
#   # --- base palette ---
#   'background':    (30, 30, 30)     # content surface / editor background
#   'foreground':    (212, 212, 212)  # primary text
#   'muted':         (157, 157, 157)  # secondary text, dividers
#   'accent':        (0, 122, 204)    # focus ring, selection fill, default bars
#   'accent2':       (78, 201, 176)   # secondary accent (i-search base, recipes)
#   'surface':       (48, 48, 52)     # raised panels (pane header / popup)
#   'selection':     (10, 105, 178)   # active selection fill
#   # --- chrome bars (a solid color for the whole bar) ---
#   'status':        (0, 122, 204)    # bottom status bar (also the viewers')
#   'footer':        (0, 122, 204)    # per-pane info bar
#   # --- file panes: per-type name colors (a sub-dict, like 'syntax';
#   #     override only the types you name) ---
#   'file_types': {'directory': (204, 204, 120),  # dirs  (default: soft yellow)
#                  'file':      (212, 212, 212),  # files (default: foreground)
#                  'link':      (86, 194, 214)}   # symlinks (default: cyan)
#   #   ('directory' may also be given as a flat top-level key — shorthand for
#   #    file_types['directory']. A symlink is colored as a link even when it
#   #    points at a directory.)
#   # --- file pane cursor cue (a sub-dict; the row outline / [ ] bracket,
#   #     distinct from the selection fill) ---
#   'cursor': {'active':   (231, 76, 76),  # focused pane (default: red)
#              'inactive': (140, 92, 94)}  # blurred pane (default: muted red)
#   # --- incremental search ---
#   'isearch_match': (78, 201, 176)   # match-highlight base (default: accent2)
#   # --- text / diff viewer syntax colors (override only the tokens you name) ---
#   'syntax': {'keyword': (86, 156, 214), 'string': (206, 145, 120),
#              'comment': (106, 153, 85), 'number': (181, 206, 168),
#              'operator': (212, 212, 212), 'builtin': (78, 201, 176),
#              'name': (156, 220, 254)}
#   # --- recommended post-processing effect (GUI backend only) ---
#   #   A full-screen CRT / phosphor "look" composited over the rendered
#   #   frame. XeFM turns it on when this theme becomes active and off when you
#   #   switch away. Only the GUI backend (`xefm/app.py --backend gui`) renders it;
#   #   a terminal has no pixels to filter and silently ignores it.
#   #     'post_effect': 'crt'       # preset: glow + bloom + scanlines + vignette + roll
#   #     'post_effect': {'bloom': 0.3, 'vignette': 0.15, 'glow': 0.22,
#   #                     'scanline': 0.15, 'roll': 0.1}  # custom (override any)
#   # --- background behind the UI (GUI backend only) ---
#   #   One background of two kinds (else the plain theme color). On/off with the
#   #   theme, like post_effect; a terminal has no pixels and ignores it. NOTE the
#   #   'background' key above is the base *color* — these choose the content:
#   #   * animation — a slow moving scene, anchored on this theme's own colors
#   #     (foreground for the scene, background for the backdrop) so it stays
#   #     on-palette:
#   #       'starfield'     stars streaming toward you, fading in with depth
#   #       'rain'          falling streaks with fading tails
#   #       'constellation' drifting nodes linked to their near neighbours
#   #       'grid'          flying through a wireframe corridor, the camera
#   #                       slowly drifting and turning as it goes
#   #       'wave'          a dense particle wave with its own colour gradient
#   #     Written as a bare type, or a dict to retune speed / opacity:
#   #       'animation': 'starfield'                     # the tuned default
#   #       'animation': {'type': 'rain', 'speed': 1.0, 'opacity': 0.8}
#   #     ('cube', a spinning wireframe, also works — it is the UI toolkit's
#   #      own reference scene rather than one of XeFM's.)
#   #   * wallpaper — a single image scaled to fill the window:
#   #       'wallpaper': '~/Pictures/bg.png'
#   #       'wallpaper': {'image': '~/bg.png', 'fit': 'fit', 'opacity': 0.8}
#   #       fit: 'fill' (cover, default) | 'fit' (contain) | 'stretch' | 'center'
#   # --- surface opacity (GUI backend only) ---
#   #   How opaque the UI's pane/row backgrounds are (0..1); below 1 the
#   #   background behind them shows through. A single per-theme value, separate
#   #   from the background so it applies to any kind. 1 = fully opaque UI.
#   #     'opacity': 0.6
#
# Example:
#
# THEMES = {
#     'Ocean': {                       # builds on Dark+
#         'accent': (38, 139, 210),
#         'file_types': {'directory': (120, 200, 220), 'link': (90, 200, 180)},
#         'syntax': {'keyword': (0, 175, 215)},
#     },
#     'Paper': {                       # a light theme, from a light base
#         'base': 'Light+',
#         'file_types': {'directory': (150, 110, 0)},
#     },
# }


# Phosphor: a monochrome phosphor-green CRT terminal — every color is a
# shade of green on a near-black screen. A ready-made example of a full
# custom theme; select it from View > Theme or with the T key. On the GUI
# backend the 'post_effect' below adds a real CRT glow over the green.

phosphor_theme = {
    "post_effect": "crt",  # CRT glow/bloom/scanlines (GUI backend)
    "animation": "rain",  # falling phosphor streaks (GUI backend)
    "opacity": 0.6,  # chrome opacity; < 1 lets the rain show through
    "background": (4, 15, 7),  # dark CRT green-black
    "foreground": (51, 245, 121),  # phosphor green
    "muted": (33, 138, 74),  # dim green (secondary text / dividers)
    "accent": (60, 235, 122),  # focus ring / selection accent
    "accent2": (124, 255, 168),  # pale mint (i-search match base)
    "surface": (11, 38, 20),  # raised panels (header / popup)
    "selection": (24, 105, 54),  # active selection fill
    "status": (12, 40, 22),  # status bar (dark green panel)
    "footer": (22, 68, 40),  # per-pane info bar (lighter, so the
    # footer/status boundary reads on TUI)
    "file_types": {
        "directory": (150, 255, 150),  # directories (brightest green)
        "link": (124, 255, 168),  # symlinks (pale mint)
    },
    "cursor": {  # keep the cue on-palette, not red
        "active": (180, 255, 180),  # bright green frame (focused pane)
        "inactive": (60, 150, 90),  # dim green frame (blurred pane)
    },
    "syntax": {
        "keyword": (130, 255, 150),
        "string": (90, 220, 120),
        "comment": (36, 140, 78),
        "number": (150, 255, 130),
        "operator": (70, 210, 110),
        "builtin": (150, 255, 170),
        "name": (60, 235, 120),
    },
}

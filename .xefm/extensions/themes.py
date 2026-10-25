"""
https://github.com/crftwr/xefm/blob/main/doc/COLOR_SCHEMES_FEATURE.ja.md
https://github.com/crftwr/xefm/blob/main/doc/CONFIGURATION_FEATURE.ja.md
"""

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

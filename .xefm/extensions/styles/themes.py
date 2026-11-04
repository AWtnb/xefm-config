# https://github.com/crftwr/xefm/blob/main/doc/COLOR_SCHEMES_FEATURE.ja.md
# https://github.com/crftwr/xefm/blob/main/doc/COLOR_SCHEMES_FEATURE.md


def _color(color: str) -> tuple[int, ...]:
    """Convert a #RRGGBB color code to an RGB tuple."""
    color = color.removeprefix("#")
    return tuple(int(color[index : index + 2], 16) for index in (0, 2, 4))


one_dark = {
    "opacity": 1.0,
    "background": _color("#282c34"),
    "foreground": _color("#abb2bf"),
    "muted": _color("#5c6370"),
    "accent": _color("#61afef"),
    "accent2": _color("#e5c07b"),
    "surface": _color("#21252b"),
    "selection": _color("#3e4451"),
    "status": _color("#21252b"),
    "footer": _color("#2c313c"),
    "file_types": {
        "directory": _color("#e06c75"),
        "link": _color("#56b6c2"),
    },
    "cursor": {
        "active": _color("#61afef"),
        "inactive": _color("#5c6370"),
    },
    "syntax": {
        "keyword": _color("#c678dd"),
        "string": _color("#98c379"),
        "comment": _color("#5c6370"),
        "number": _color("#d19a66"),
        "operator": _color("#56b6c2"),
        "builtin": _color("#e5c07b"),
        "name": _color("#e06c75"),
    },
}


tokyo_night = {
    "opacity": 1.0,
    "background": _color("#1a1b26"),
    "foreground": _color("#c0caf5"),
    "muted": _color("#565f89"),
    "accent": _color("#7aa2f7"),
    "accent2": _color("#e0af68"),
    "surface": _color("#16161e"),
    "selection": _color("#283457"),
    "status": _color("#16161e"),
    "footer": _color("#1f2335"),
    "file_types": {
        "directory": _color("#7aa2f7"),
        "link": _color("#7dcfff"),
    },
    "cursor": {
        "active": _color("#7aa2f7"),
        "inactive": _color("#565f89"),
    },
    "syntax": {
        "keyword": _color("#bb9af7"),
        "string": _color("#9ece6a"),
        "comment": _color("#565f89"),
        "number": _color("#ff9e64"),
        "operator": _color("#89ddff"),
        "builtin": _color("#7dcfff"),
        "name": _color("#f7768e"),
    },
}

THEMES = {"One Dark": one_dark, "Tokyo Night": tokyo_night}

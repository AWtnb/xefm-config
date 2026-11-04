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

ayu_dark = {
    "opacity": 1.0,
    "background": _color("#0b0e14"),
    "foreground": _color("#bfbdb6"),
    "muted": _color("#565b66"),
    "accent": _color("#e6b450"),
    "accent2": _color("#ffb454"),
    "surface": _color("#0d1017"),
    "selection": _color("#273747"),
    "status": _color("#0d1017"),
    "footer": _color("#131721"),
    "file_types": {
        "directory": _color("#59c2ff"),
        "link": _color("#95e6cb"),
    },
    "cursor": {
        "active": _color("#e6b450"),
        "inactive": _color("#565b66"),
    },
    "syntax": {
        "keyword": _color("#ff8f40"),
        "string": _color("#aad94c"),
        "comment": _color("#5c6773"),
        "number": _color("#d2a6ff"),
        "operator": _color("#f29668"),
        "builtin": _color("#59c2ff"),
        "name": _color("#ffb454"),
    },
}

ayu_mirage = {
    "opacity": 1.0,
    "background": _color("#1f2430"),
    "foreground": _color("#cccac2"),
    "muted": _color("#707a8c"),
    "accent": _color("#ffcc66"),
    "accent2": _color("#ffad66"),
    "surface": _color("#1a1f29"),
    "selection": _color("#33415e"),
    "status": _color("#1a1f29"),
    "footer": _color("#dfbfff"),
    "file_types": {
        "directory": _color("#73d0ff"),
        "link": _color("#95e6cb"),
    },
    "cursor": {
        "active": _color("#ffcc66"),
        "inactive": _color("#707a8c"),
    },
    "syntax": {
        "keyword": _color("#ffad66"),
        "string": _color("#d5ff80"),
        "comment": _color("#6e7c8e"),
        "number": _color("#dfbfff"),
        "operator": _color("#f29e74"),
        "builtin": _color("#73d0ff"),
        "name": _color("#ffd173"),
    },
}

cobalt2 = {
    "opacity": 1.0,
    "background": _color("#193549"),
    "foreground": _color("#ffffff"),
    "muted": _color("#0088ff"),
    "accent": _color("#ffc600"),
    "accent2": _color("#ff9d00"),
    "surface": _color("#15232d"),
    "selection": _color("#0d3a58"),
    "status": _color("#15232d"),
    "footer": _color("#1f4662"),
    "file_types": {
        "directory": _color("#9effff"),
        "link": _color("#80ffbb"),
    },
    "cursor": {
        "active": _color("#ffc600"),
        "inactive": _color("#0088ff"),
    },
    "syntax": {
        "keyword": _color("#ff9d00"),
        "string": _color("#3ad900"),
        "comment": _color("#0088ff"),
        "number": _color("#ff628c"),
        "operator": _color("#ff9d00"),
        "builtin": _color("#80ffbb"),
        "name": _color("#ffc600"),
    },
}

THEMES = {
    "One Dark": one_dark,
    "Tokyo Night": tokyo_night,
    "Ayu Dark": ayu_dark,
    "Ayu Mirage": ayu_mirage,
    "Cobalt2": cobalt2,
}

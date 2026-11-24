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

palette_base16_darkmoss = {
    "base00": _color("#171e1f"),
    "base01": _color("#252c2d"),
    "base02": _color("#373c3d"),
    "base03": _color("#555e5f"),
    "base04": _color("#818f80"),
    "base05": _color("#c7c7a5"),
    "base06": _color("#e3e3c8"),
    "base07": _color("#e1eaef"),
    "base08": _color("#ff4658"),
    "base09": _color("#e6db74"),
    "base0A": _color("#fdb11f"),
    "base0B": _color("#499180"),
    "base0C": _color("#66d9ef"),
    "base0D": _color("#498091"),
    "base0E": _color("#9bc0c8"),
    "base0F": _color("#d27b53"),
}

base16_darkmoss = {
    "opacity": 1.0,
    "background": palette_base16_darkmoss["base00"],
    "foreground": palette_base16_darkmoss["base05"],
    "muted": palette_base16_darkmoss["base03"],
    "accent": palette_base16_darkmoss["base0D"],
    "accent2": palette_base16_darkmoss["base0A"],
    "surface": palette_base16_darkmoss["base01"],
    "selection": palette_base16_darkmoss["base02"],
    "status": palette_base16_darkmoss["base01"],
    "footer": palette_base16_darkmoss["base02"],
    "file_types": {
        "directory": palette_base16_darkmoss["base09"],
        "link": palette_base16_darkmoss["base0C"],
    },
    "cursor": {
        "active": palette_base16_darkmoss["base08"],
        "inactive": palette_base16_darkmoss["base03"],
    },
    "syntax": {
        "keyword": palette_base16_darkmoss["base0E"],
        "string": palette_base16_darkmoss["base0B"],
        "comment": palette_base16_darkmoss["base03"],
        "number": palette_base16_darkmoss["base09"],
        "operator": palette_base16_darkmoss["base0C"],
        "builtin": palette_base16_darkmoss["base0A"],
        "name": palette_base16_darkmoss["base08"],
    },
}

palette_base16_0x96f = {
    "base00": _color("#262427"),
    "base01": _color("#3b393c"),
    "base02": _color("#514f52"),
    "base03": _color("#676567"),
    "base04": _color("#7c7b7d"),
    "base05": _color("#fcfcfc"),
    "base06": _color("#eae9eb"),
    "base07": _color("#fcfcfc"),
    "base08": _color("#ff7272"),
    "base09": _color("#fc9d6f"),
    "base0A": _color("#ffca58"),
    "base0B": _color("#bcdf59"),
    "base0C": _color("#aee8f4"),
    "base0D": _color("#49cae4"),
    "base0E": _color("#a093e2"),
    "base0F": _color("#ff8787"),
}

base16_0x96f = {
    "opacity": 1.0,
    "background": palette_base16_0x96f["base00"],
    "foreground": palette_base16_0x96f["base05"],
    "muted": palette_base16_0x96f["base03"],
    "accent": palette_base16_0x96f["base0D"],
    "accent2": palette_base16_0x96f["base0A"],
    "surface": palette_base16_0x96f["base00"],
    "selection": palette_base16_0x96f["base02"],
    "status": palette_base16_0x96f["base01"],
    "footer": palette_base16_0x96f["base02"],
    "file_types": {
        "directory": palette_base16_0x96f["base0B"],
        "link": palette_base16_0x96f["base0C"],
    },
    "cursor": {
        "active": palette_base16_0x96f["base08"],
        "inactive": palette_base16_0x96f["base03"],
    },
    "syntax": {
        "keyword": palette_base16_0x96f["base0E"],
        "string": palette_base16_0x96f["base0B"],
        "comment": palette_base16_0x96f["base03"],
        "number": palette_base16_0x96f["base09"],
        "operator": palette_base16_0x96f["base0C"],
        "builtin": palette_base16_0x96f["base0A"],
        "name": palette_base16_0x96f["base08"],
    },
}

THEMES = {
    "Ayu Dark": ayu_dark,
    "Ayu Mirage": ayu_mirage,
    "Base16 0x96f": base16_0x96f,
    "Base16 Darkmoss": base16_darkmoss,
    "Cobalt2": cobalt2,
    "One Dark": one_dark,
    "Tokyo Night": tokyo_night,
}

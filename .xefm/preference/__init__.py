from . import favorite, keybind, theme

THEMES = {"Phosphor": theme.phosphor_theme}

KEY_BINDINGS = keybind.bindings

FAVORITE_DIRECTORIES = favorite.get_okini_bookmarks() or []

from pathlib import Path

from . import favorite, keybind, theme
from ._utils import smart_check_path

THEMES = {"Phosphor": theme.phosphor_theme}

KEY_BINDINGS = keybind.bindings

OKINI_BOOKMARKS = favorite.get_okini_bookmarks() or []

FAVORITE_DIRECTORIES = [
    fav
    for fav in OKINI_BOOKMARKS
    if smart_check_path(fav["path"]) and Path(fav["path"]).is_dir()
]

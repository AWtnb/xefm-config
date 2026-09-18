from . import action, assoc, event_hook, favorite, filter, keybind, sort_key, theme

THEMES = {"Phosphor": theme.phosphor_theme}

KEY_BINDINGS = keybind.bindings

OKINI_BOOKMARKS = favorite.get_okini_bookmarks() or []

FAVORITE_DIRECTORIES = [fav for fav in OKINI_BOOKMARKS]

ACTIONS = action.actions

EVENT_HOOKS = event_hook.event_hooks

SORT_KEYS = sort_key.sort_keys

FILTERS = filter.filters

FILE_ASSOCIATIONS = assoc.file_associations

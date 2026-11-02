from . import layouts, themes


def setup() -> tuple:
    return (
        themes.THEMES,
        layouts.DEFAULT_LAYOUT,
        layouts.ATTRIBUTES,
        layouts.LAYOUTS,
        layouts.LAYOUT_EXTRAS,
    )

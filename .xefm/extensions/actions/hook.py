import json
import os

from xefm import favorites  # ty: ignore[unresolved-import]


def on_enter(ctx, event) -> bool:
    if event.path.suffix.lower() in [".pdf", ".tbx", ".cmx"]:
        ctx.invoke("open_with_os")
        return True
    return False


def backup_favorites_on_quit(ctx, _) -> bool:

    favs = favorites.get_favorites()  # list[FavoriteEntry]
    rows = [
        {"name": f.name, "path": f.path, "is_file": f.is_file, "origin": f.origin}
        for f in favs
    ]

    path = os.path.expanduser("~/xefm-favs-backup.json")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
    except Exception as e:  # noqa: BLE001
        ctx.message(f"Failed to backup favorites: {e}")

    return False

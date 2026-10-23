import json
import os

from xefm import favorites  # ty: ignore[unresolved-import]

# --- EVENT_HOOKS ------------------------------------------------------
# Functions run at set moments. Each event maps to a list, run in order.
#
# Every hook is fn(ctx, event); what happened is on the event:
#
#   'startup'           (nothing more)     once the app is up
#   'quit'              (nothing more)     before XeFM shuts down
#   'directory_changed' event.pane, event.old_path, event.new_path
#   'file_open'         event.path         return True to claim the open
#
# 'file_open' fires before XeFM decides what to do with a file, so returning
# True is how you route one file type somewhere of your own without touching
# FILE_ASSOCIATIONS. It does not fire for directories -- entering one is
# navigation, not opening.
#
# def log_visit(ctx, event):
#     with open(Path.home() / '.xefm' / 'visited.log', 'a') as f:
#         f.write(f"{event.new_path}\n")
#
# def open_psd_in_gimp(ctx, event):
#     if event.path.suffix.lower() != '.psd':
#         return False
#     subprocess.Popen(['gimp', str(event.path)])
#     return True                 # claimed -- XeFM does nothing further
#
# EVENT_HOOKS = {
#     'directory_changed': [log_visit],
#     'file_open': [open_psd_in_gimp],
# }


def _smart_enter(ctx, event) -> bool:
    if event.path.suffix.lower() in [".pdf", ".tbx", ".cmx"]:
        ctx.invoke("open_with_os")
        return True
    return False


def _backup_favorites_on_quit(ctx, _) -> bool:

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


event_hooks = {
    "quit": [_backup_favorites_on_quit],
    "file_open": [_smart_enter],
}

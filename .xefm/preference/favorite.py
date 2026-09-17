import json
import os

from ._utils import smart_check_path


def get_okini_bookmarks() -> list[dict[str, str]] | None:
    bookmark_json = os.path.expandvars(r"${APPDATA}\okini\bookmarks.json")
    if not smart_check_path(bookmark_json):
        return None

    with open(bookmark_json, "r", encoding="utf-8") as f:
        return json.load(f)

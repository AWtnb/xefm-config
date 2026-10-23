import os
import shutil
import subprocess
from pathlib import Path
from typing import NamedTuple

from libs.cursor_jump import focus_newest_item, jump_down, jump_up
from libs.item_selector import select_only_dirs, select_only_files, select_under_cursor
from libs.tree import make_tree, summarize_by

# --- ACTIONS ----------------------------------------------------------
# A function takes one argument, the context object, and is run on the UI
# thread while XeFM waits -- so keep it quick. Anything it raises is logged
# with a traceback and dropped; it never takes XeFM down.
#
# Define the functions ABOVE `class Config:` (module level), then:
#
# def select_documents(ctx):
#     """Select every Word/PDF document in the active pane."""
#     n = ctx.pane.select(lambda e: e.suffix.lower() in ('.docx', '.pdf'))
#     ctx.message(f"Selected {n} document(s)")
#
# def go_to_sibling(ctx):
#     """Point the other pane at this pane's directory."""
#     ctx.other.cd(ctx.pane.path)
#
# ACTIONS = {
#     'select-documents': select_documents,
#     'go-to-sibling': go_to_sibling,
# }
# ...and bind them in KEY_BINDINGS above, like any built-in action:
#     'select-documents': ['Shift-Y'],
#
# Every action of yours is in the command palette (Ctrl-T), key or no
# key. The docstring is how it is described there: its first line is the
# one-line description (also the Help dialog's row), and the paragraphs
# after a blank line are the page F1 opens in the palette (Markdown):
#
# def open_in_vscode(ctx):
#     """Open the item under the cursor in VS Code.
#
#     Works on directories too -- VS Code opens them as a workspace.
#     """
#     ctx.run_program(['code', str(ctx.pane.focused.path)])
#
# Without a docstring the palette has only the name to show. (The dict
# form below also takes a 'description', written and split the same way,
# which replaces the docstring -- for a function that cannot carry one,
# such as a lambda.)
#
# An action name that already exists is ignored unless you say you meant it,
# which also keeps the built-in reachable so you can wrap it:
#
# def confirm_then_quit(ctx):
#     ctx.message("see you")
#     ctx.invoke('quit')          # runs the built-in 'quit'
#
# ACTIONS = {'quit': {'func': confirm_then_quit, 'override': True}}
#
# What the context object offers:
#   ctx.pane / ctx.other / ctx.left / ctx.right   the panes
#   ctx.invoke(name)                              run another action
#   ctx.message(text)                             one line in the log pane
#   ctx.input(prompt, default, on_accept=fn)      ask for text
#   ctx.choose(title, items, on_result=fn)        pick from a list
#   ctx.confirm(prompt, on_result=fn)             yes / no
#   ctx.run_program(['cmd', ...], terminal=False) run an external program;
#       terminal=True lends it the terminal (vim, massren...) and waits.
#       Don't subprocess.run() one yourself -- the screen breaks.
# ...and on each pane:
#   pane.path, pane.entries, pane.cursor, pane.focused, pane.selected()
#   pane.select(predicate) / pane.unselect(predicate) / pane.refresh()
#   pane.cd(path, focus_name=None)
# Each entry has .name, .path, .suffix, .stem, .is_dir, .is_file, .is_link,
# .size and .mtime.
#
# XeFM never blocks on a dialog, so input/choose/confirm hand their answer to
# a callback instead of returning it -- put the rest of the action in there.


def open_in_vscode(ctx) -> None:
    """Open current dir in VS Code."""
    ctx.run_program(["code", str(ctx.pane.path)])


def _select_by_focus(ctx) -> None:
    focused = ctx.pane.focused
    if focused.is_dir:
        select_only_dirs(ctx)
    else:
        select_only_files(ctx)


def smart_select_all(ctx) -> None:
    selected = ctx.pane.selected()

    if not selected:
        _select_by_focus(ctx)
        return

    if len(selected) == len(ctx.pane.entries):
        return

    selected_paths = [ent.path for ent in selected]
    dir_paths = [ent.path for ent in ctx.pane.entries if ent.is_dir]
    file_paths = [ent.path for ent in ctx.pane.entries if not ent.is_dir]

    is_all_dir_selected = len(dir_paths) != 0 and all(
        ent in selected_paths for ent in dir_paths
    )
    is_all_file_selected = len(file_paths) != 0 and all(
        ent in selected_paths for ent in file_paths
    )
    if is_all_dir_selected or is_all_file_selected:
        ctx.invoke("select_all")
        return

    _select_by_focus(ctx)


DESKTOP_PATH = os.path.expanduser(r"~/Desktop")


def quick_copy(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("copy_files")


def quick_move(ctx) -> None:
    if not ctx.pane.selected():
        select_under_cursor(ctx)
    ctx.invoke("move_files")


def open_desktop(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)
    ctx.other.cd(DESKTOP_PATH)
    ctx.invoke("reset_pane_boundary")


def open_ghq_repo(ctx) -> None:
    ghq_root = Path(os.path.expanduser(r"~/ghq"))
    if not ghq_root.is_dir():
        ctx.message(f"ghq root not found: {ghq_root}")
        return

    ghq_cmd = shutil.which("ghq")
    if ghq_cmd is None:
        ctx.message("ghq is not installed or not in PATH.")
        return
    try:
        out = subprocess.check_output(
            [ghq_cmd, "list", "--full-path"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except Exception as exc:  # noqa: BLE001
        ctx.message(f"ghq failed: {exc}")
        return

    class RepoPath(NamedTuple):
        rel: str
        full: str

        @classmethod
        def from_path(cls, path: str):
            rel = Path(path).relative_to(ghq_root)
            return cls(str(rel), path)

    repo_paths = [
        RepoPath.from_path(line.strip()) for line in out.splitlines() if line.strip()
    ]
    if not repo_paths:
        ctx.message("No repositories found under ~/ghq.")
        return

    def _on_select(index):
        if index is None:
            return
        ctx.pane.cd(repo_paths[index].full)

    ctx.choose(
        "Select ghq repository",
        [r.rel for r in repo_paths],
        type="filter",
        on_result=_on_select,
    )


actions = {
    "open_in_vscode": open_in_vscode,
    "open_desktop": open_desktop,
    "open_desktop_both": open_desktop_both,
    "open_ghq_repo": open_ghq_repo,
    "focus_newest_item": focus_newest_item,
    "jump_down": jump_down,
    "jump_up": jump_up,
    "make_tree": make_tree,
    "summarize_by": summarize_by,
    "quick_copy": quick_copy,
    "quick_move": quick_move,
    "smart_select_all": smart_select_all,
}

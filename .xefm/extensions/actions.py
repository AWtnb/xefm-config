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


import os


def open_in_vscode(ctx) -> None:
    """Open current dir in VS Code."""
    ctx.run_program(["code", str(ctx.pane.path)])


def smart_enter(ctx) -> None:
    item = ctx.pane.focused
    if not item:
        return

    supported_extensions = [".pdf", ".docx", ".xlsx"]
    ext = item.path.suffix.lower()
    if ext in supported_extensions:
        os.startfile(item.path)
        return

    ctx.invoke("open_item")


DESKTOP_PATH = os.path.expanduser(r"~/Desktop")


def open_desktop(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)


def open_desktop_both(ctx) -> None:
    ctx.pane.cd(DESKTOP_PATH)
    ctx.other.cd(DESKTOP_PATH)


actions = {
    "open_in_vscode": open_in_vscode,
    "smart_enter": smart_enter,
    "open_desktop": open_desktop,
    "open_desktop_both": open_desktop_both,
}

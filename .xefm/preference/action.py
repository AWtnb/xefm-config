# -----------------------------------------------------------------------
# In-process customization -- PREVIEW
# -----------------------------------------------------------------------
# This config file is executed Python, so it can define functions as well as
# settings. ACTIONS binds your own functions to action names (which
# KEY_BINDINGS above then binds to keys, exactly like a built-in action), and
# EVENT_HOOKS runs them at set moments in XeFM's life.
#
# PREVIEW: this is not a stable API yet. The objects passed to your functions
# and the shape of these two variables may change in any release until
# xefm.user_api.API_VERSION reaches 1. XeFM logs one line saying so when a
# config uses either variable. Everything else in this file is unaffected.
#
# Both reload with the rest of the config ('reload_config'), so iterating on
# an action is edit-then-reload -- no restart.
#
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
#     'select-documents': ['Shift-D'],
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
# ...and on each pane:
#   pane.path, pane.entries, pane.cursor, pane.focused, pane.selected()
#   pane.select(predicate) / pane.unselect(predicate) / pane.refresh()
#   pane.cd(path, focus_name=None)
# Each entry has .name, .path, .suffix, .stem, .is_dir, .is_file, .is_link,
# .size and .mtime.
#
# XeFM never blocks on a dialog, so input/choose/confirm hand their answer to
# a callback instead of returning it -- put the rest of the action in there.

actions = {}

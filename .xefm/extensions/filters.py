# --- FILTERS ----------------------------------------------------------
# Your own filters. Each one becomes a fixed row in the Filter dialog (';'),
# under "clear filter" and above the patterns you have typed there before.
#
# The simple kind is one or more wildcard patterns:
#
# FILTERS = {
#     'images': ['*.jpg', '*.jpeg', '*.png', '*.gif'],   # any one matches
# }
#
# The other kind is a function, which is how you filter by something the
# name does not say -- size, date, whatever you can work out from the entry.
# It takes one entry and returns True to show it:
#
# import time                              # at the top of this file
#
# def modified_today(entry):
#     return entry.mtime >= time.time() - 24 * 3600
#
# FILTERS = {
#     'today': {'label': 'Modified today', 'match': modified_today},
#     'big': {'label': 'Over 100 MB', 'match': lambda e: e.size > 100 << 20},
# }
#
# 'label' is the row text and defaults to the name you gave it. An entry has
# the same fields a sort key sees -- .name, .path, .suffix, .stem, .is_dir,
# .is_file, .is_link, .size and .mtime -- and reading .size or .mtime is free.
#
# Directories are always shown, exactly as they are under a typed pattern: a
# filter that hid them would take away the folder you were about to open. So
# your function only decides which files are visible -- and "directories
# only" is written 'match': lambda e: False.
#
# A name may not contain * ? or [ -- XeFM remembers a filter by its name and
# a typed pattern as itself, and one that read as both could not be told
# apart. Put the wildcards in 'pattern' and give the filter a plain name.
#
# Like a sort key, a filter function runs on a background thread, so keep it
# to arithmetic and strings. One that fails loses the filter rather than the
# listing: the pane shows everything and says so once in the log pane --
# deliberately that way round, so a broken filter never hides files from an
# operation you are about to run.

filters = {}

# --- SORT_KEYS --------------------------------------------------------
# Your own sort orders. Each one becomes a row in the sort dialog ('s') and
# in the Sort By menu, alongside Filename / Extension / Size / Timestamp.
#
# A sort key takes one entry and returns anything that can be compared --
# XeFM sorts by whatever comes back. Return a tuple for a multi-level order;
# tuples compare item by item, so (e.size, e.name) means "by size, and by
# name within the same size".
#
# def size_then_name(entry):
#     return (entry.size, entry.name)
#
# SORT_KEYS = {
#     'biggest': {'label': 'Size, then name', 'key': size_then_name},
# }
#
# Two things you do NOT have to handle: directories always come first, and
# ascending/descending is applied for you. Your key only decides the order
# inside one group. Reading entry.size or entry.mtime is free -- XeFM already
# collected them for the listing.
#
# Naming one of the four built-in sorts -- 'filename', 'extension', 'size',
# 'timestamp', the dialog's own rows in lower case -- replaces it, which
# needs 'override': True so a typo cannot quietly change what Filename means. XeFM orders names by character code, which is not how
# Explorer or Finder order a directory; this is where you change that:
#
# import locale, re                       # at the top of this file
# locale.setlocale(locale.LC_COLLATE, '')  # your system's own ordering
#
# def by_system_order(entry):
#     # digit runs as numbers, everything else through the system's ordering
#     parts = re.split(r'(\d+)', entry.name)
#     return [int(p) if i % 2 else locale.strxfrm(p) for i, p in enumerate(parts)]
#
# SORT_KEYS = {'filename': {'key': by_system_order, 'override': True}}
#
# That follows your locale, which is close to but not the same as the shell's
# own order. Matching Explorer or Finder exactly means their comparison
# functions -- StrCmpLogicalW and localizedStandardCompare: -- which compare
# two names rather than producing a key, so wrap one in
# functools.cmp_to_key(...) and expect it to cost more on a large directory.
#
# The rest of an entry: 'label' is the row text (defaults to the name),
# 'explain' is the example line the dialog shows under the order, and
# 'hotkey' is a letter that applies the sort straight from the dialog (a new
# row gets its label's initial when no other row has claimed it).
#
# A key runs on a background thread, so keep it to arithmetic and strings.
# One that fails, or returns things that cannot be compared with each other,
# loses the sort rather than the listing: the pane falls back to ordering by
# filename and says so once in the log pane.

sort_keys = {}

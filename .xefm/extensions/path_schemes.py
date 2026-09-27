# --- PATH_SCHEMES -----------------------------------------------------
# Your own browsable locations. A scheme like 'reg' makes 'reg://...' a
# place XeFM can open in a pane, jump to (Shift-J), and keep in FAVORITE_
# DIRECTORIES -- listed by your class rather than read off a disk.
#
# Inherit ReadOnlyPathImpl and write five methods. Everything else -- the
# path arithmetic, refusing writes, what the pane and the status bar show --
# comes with it.
#
# Define the class ABOVE `class Config:` (module level), with anything it
# reads. Inside the class body it would *load* fine and then fail on every
# call: a class body is not a scope the methods defined in it can see, so
# NOTES and io below would come back as NameError the first time XeFM asked
# the folder a question.
#
#     import io
#     from xefm.path_base import ReadOnlyPathImpl, UriStatResult
#
#     NOTES = {'': ['todo', 'ideas'], 'todo': [], 'ideas': []}
#
#     class NotesPathImpl(ReadOnlyPathImpl):
#         def exists(self):   return self._key in NOTES
#         def is_dir(self):   return self._key in NOTES
#         def iterdir(self):
#             for name in NOTES.get(self._key, []):
#                 yield self._child(name)
#         def stat(self):     return UriStatResult(is_dir=self.is_dir())
#         def open(self, mode='r', buffering=-1, encoding=None,
#                  errors=None, newline=None):
#             return io.StringIO('')
#
#     class Config:
#         ...
#
# Then name it here -- this line, in the class, is the only part that
# belongs at this indentation:
#
#     PATH_SCHEMES = {'notes': NotesPathImpl}
#
# self._key is the part after 'notes://', with no leading or trailing
# slash -- '' at the root, 'todo/monday' further in. self._child(name)
# builds a child; XeFM works out parents, names and suffixes itself.
#
# Writing is refused for you, with a clear message. Say why in your own
# words with READ_ONLY_MESSAGE = 'edit these in the Notes app'.
#
# A class that is missing one of the five methods, or whose scheme name is
# not a valid one, is skipped with a line in the log pane -- the rest of
# your config still loads. A method that *raises* is reported the same way,
# with its traceback, when something asks the folder a question.
# See doc/VIRTUAL_FOLDERS_FEATURE.md.

path_schemes = {}

# --- LEXERS -----------------------------------------------------------
# Syntax highlighting for files the text viewer shows as plain text, or
# colors as the wrong language. The coloring comes from Pygments, which
# knows hundreds of languages; this names the lexer for a file name.
#
# The key is a file-name pattern ('*.mnl', or just '.mnl'; 'Jenkinsfile'
# for a name with no suffix). The value is either the name of a lexer
# Pygments already has -- `pygmentize -L lexers` lists them -- or a lexer
# class of your own:
#
#     from autocad_lexers import DclLexer   # at the top of this file
#
#     LEXERS = {
#         '*.dcl': DclLexer,      # your own lexer
#         '*.mnl': 'newlisp',     # an existing one, for another suffix
#     }
#
# Your own lexer is an ordinary Pygments lexer -- a RegexLexer subclass,
# written the way https://pygments.org/docs/lexerdevelopment/ describes,
# with nothing from XeFM in it. Keep it in its own file in
# ~/.xefm/extensions/ (autocad_lexers.py above) and import it here. Its
# own `filenames` attribute is not used: the key here alone decides which
# files it colors. Its `aliases` are -- once registered, its alias can be
# a value here too ('*.dclx': 'dcl').
#
# An entry here wins over Pygments' own choice for the same files, which
# is how you recolor a suffix Pygments gives to another language. An
# entry naming a lexer that does not exist is skipped with a line in the
# log pane.

lexers = {}

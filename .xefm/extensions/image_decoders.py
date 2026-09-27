
# --- IMAGE_DECODERS ---------------------------------------------------
# Picture formats the built-in image viewer does not read yet.
#
# It already reads a lot without help, and which formats depends on your
# machine rather than on XeFM: on macOS it draws HEIC, JPEG XL and camera
# RAW through the system's own decoder; on Windows through whichever WIC
# codecs are installed (the HEIF and AV1 extensions from the Store, if you
# have them); in a terminal through Pillow, including any Pillow plugin you
# installed. Installing pillow-heif is enough to add HEIC anywhere:
#
#     pip install pillow-heif
#
# What is left after all that is the formats only a library XeFM does not
# ship can read. Write a function that turns the file's bytes into a
# picture, and name the suffix it is for:
#
#     import io                             # at the top of this file
#
#     def open_svg(data):
#         import cairosvg
#         from PIL import Image
#         return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=data)))
#
#     def open_raw(data):
#         import rawpy
#         from PIL import Image
#         with rawpy.imread(io.BytesIO(data)) as raw:
#             return Image.fromarray(raw.postprocess())
#
#     IMAGE_DECODERS = {
#         '.svg': open_svg,
#         '.dng': open_raw,
#         '.cr2': open_raw,
#     }
#
# Your function gets the file's bytes -- not a path -- so the same decoder
# works on a picture inside a zip or on an S3 bucket, with nothing copied to
# a temp file first. Return a PIL.Image (the usual answer), or None for "I
# cannot read this one".
#
# Registering a suffix is also what makes the viewer OFFER that format:
# Enter on a .dng opens the picture rather than the binary viewer. XeFM only
# ever claims formats something on the machine can actually decode, so it
# never opens onto an "I cannot show this" card.
#
# Registering a suffix XeFM already reads replaces its decoder with yours --
# that is how you override how a format is read, and it is the only way.
#
# Like a sort key or a filter, a decoder may run on a background thread, so
# it must not touch the UI. One that fails costs that picture and nothing
# else: the viewer shows the reason on its card and the log pane gets the
# traceback.
image_decoders = {}
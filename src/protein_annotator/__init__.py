from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("protein_annotator")
except PackageNotFoundError:
    __version__ = "unknown version"

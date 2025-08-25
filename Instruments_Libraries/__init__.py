# Instruments_Libraries/__init__.py
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0+unknown"  # fallback for source (e.g., docs/CI)

# __all__
__all__ = [
    "__version__",
]
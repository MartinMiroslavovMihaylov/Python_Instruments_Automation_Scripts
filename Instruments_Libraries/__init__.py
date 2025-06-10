# Instruments_Libraries/__init__.py
import importlib.metadata as _metadata

__version__ = _metadata.version(__name__)
__all__ = ["__version__"]

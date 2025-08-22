# Instruments_Libraries/__init__.py
import importlib.metadata as _metadata

__version__ = _metadata.version(__name__)

# Import submodules here to make them accessible from the top level
# e.g. import Instruments_Libraries.APPH
from . import APPH
from . import AQ6370D
from . import CoBrite
from . import FSWP50
from . import GPP4323
from . import InstrumentSelect
from . import KA3005
from . import KA3005p
from . import KEITHLEY2612
from . import LU1000
from . import M8070B
from . import MG3694C
from . import MS2760A
from . import MS4647B
from . import PM100D
from . import RD3005
from . import SMA100B
from . import UXR

# Directly import core classes/functions to make them available at the top level
# e.g. from Instruments_Libraries import APPH
from .APPH import APPH
from .AQ6370D import AQ6370D
from .CoBrite import CoBrite
from .FSWP50 import FSWP50
from .GPP4323 import GPP4323
from .KA3005 import KA3005
from .KA3005p import KA3005p
from .KEITHLEY2612 import KEITHLEY2612
from .LU1000 import LU1000_Cband, LU1000_Oband
from .M8070B import M8070B
from .MG3694C import MG3694C
from .MS2760A import MS2760A
from .MS4647B import MS4647B
from .PM100D import PM100D
from .RD3005 import RD3005
from .SMA100B import SMA100B
from .UXR import UXR

# __all__
__all__ = [
    "__version__",
    "APPH",
    "AQ6370D",
    "CoBrite",
    "FSWP50",
    "GPP4323",
    "KA3005",
    "KA3005p",
    "KEITHLEY2612",
    "LU1000",
    "LU1000_Cband",
    "LU1000_Oband",
    "M8070B",
    "MG3694C",
    "MS2760A",
    "MS4647B",
    "PM100D",
    "RD3005",
    "SMA100B",
    "UXR",
]

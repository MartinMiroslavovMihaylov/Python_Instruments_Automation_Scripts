"""
Created on Mon Jan 31 08:55:42 2022
Refactored on Tue Feb 27 2025

@author: Martin.Mihaylov
@author: Maxim Weizel
"""

from __future__ import annotations

import logging
import re
import typing 
import pyvisa as visa

if typing.TYPE_CHECKING:
    from Instruments_Libraries.APPH import APPH
    from Instruments_Libraries.AQ6370D import AQ6370D
    from Instruments_Libraries.CoBrite import CoBrite
    from Instruments_Libraries.FSWP50 import FSWP50
    from Instruments_Libraries.GPP4323 import GPP4323
    from Instruments_Libraries.KEITHLEY2612 import KEITHLEY2612
    from Instruments_Libraries.LU1000 import LU1000_Cband
    from Instruments_Libraries.MG3694C import MG3694C
    from Instruments_Libraries.MS2760A import MS2760A
    from Instruments_Libraries.MS4647B import MS4647B
    from Instruments_Libraries.PM100D import PM100D
    from Instruments_Libraries.RD3005 import RD3005
    from Instruments_Libraries.SMA100B import SMA100B
    from Instruments_Libraries.UXR import UXR

from pyvisa.errors import VisaIOError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# Auto-Discovery Helper
# =============================================================================


def find_resource(model_regex: str, resource_filter: str = "?*INSTR", specific_address: str | None = None) -> str:
    """
    Find a VISA resource matching the given model regex.
    If specific_address is provided, it is returned directly (after verification if possible).
    Returns the matching VISA resource string.
    """
    import pyvisa  # <- ensure pyvisa is defined in this scope
    rm = pyvisa.ResourceManager()
    
    if specific_address:
        logger.info(f"Using specific address: {specific_address}")
        return specific_address

    try:
        resources = rm.list_resources(resource_filter)
    except ValueError:
        resources = []

    logger.info(f"Scanning {len(resources)} resources for pattern '{model_regex}'...")

    for res in resources:
        # Only consider TCPIP and relevant serial ports
        if not (res.startswith("TCPIP") or res.startswith("ASRL")):
            continue

        try:
            with rm.open_resource(res) as inst:
                inst.timeout = 500  # ms
                idn = None
                try:
                    idn = inst.query("*IDN?").strip()
                except Exception:
                    pass

                if idn and re.search(model_regex, idn, re.IGNORECASE):
                    logger.info(f"Found match at {res}: {idn}")
                    return res
        except Exception:
            continue

    # Last-resort fallback for link-local (169.254.x.x) devices if auto-discovery fails
    link_local_candidates = [r for r in resources if r.startswith("TCPIP::169.254.")]
    for res in link_local_candidates:
        try:
            with rm.open_resource(res) as inst:
                inst.timeout = 500
                idn = inst.query("*IDN?").strip()
                if idn and re.search(model_regex, idn, re.IGNORECASE):
                    logger.info(f"Found link-local match at {res}: {idn}")
                    return res
        except Exception:
            continue

    raise RuntimeError(f"No instrument found matching pattern: {model_regex}")

# =============================================================================
# Instrument Factory Functions
# =============================================================================


def OSA(resource: str | None = None) -> "AQ6370D":
    """
    Connect to Yokogawa AQ6370D.
    Priority:
      1. Use user-provided resource
      2. Auto-discovery
      3. Fallback to known link-local IPs
    """
    from Instruments_Libraries.AQ6370D import AQ6370D
    import pyvisa  # <- ensure pyvisa is defined in this scope


    if resource:
        logger.info(f"User provided resource: {resource}")
        return AQ6370D(resource)

    # 1️⃣ Try auto-discovery
    try:
        resource = find_resource(r"AQ6370")
        logger.info(f"AQ6370D found via auto-discovery: {resource}")
        return AQ6370D(resource)
    except RuntimeError:
        logger.warning("AQ6370D not found by auto-discovery.")

    # 2️⃣ Try fallback IPs observed in PyVISA
    fallback_ips = [
        "TCPIP::169.254.2.21::INSTR",   # current device seen on pyvisa
        "TCPIP::169.254.58.101::INSTR"  # legacy fallback (optional)
    ]

    for ip in fallback_ips:
        try:
            logger.info(f"Trying fallback IP: {ip}")
            return AQ6370D(ip)
        except Exception as e:
            logger.warning(f"Failed to connect to {ip}: {e}")

    raise RuntimeError(
        "AQ6370D could not be found. Please provide the correct resource string "
        "or ensure the device is on the network and responds to *IDN? queries."
    )

def Laser_CoBrite(resource: str | None = None) -> CoBrite:  # noqa: N802
    from Instruments_Libraries.CoBrite import CoBrite

    if resource is None:
        resource = find_resource(r"COBRITE")
    return CoBrite(resource)


def SourceMeter(resource: str | None = None) -> KEITHLEY2612:  # noqa: N802
    from Instruments_Libraries.KEITHLEY2612 import KEITHLEY2612

    if resource is None:
        resource = find_resource(r"Keithley.*2612")
    return KEITHLEY2612(resource)





def PowerSupply(resource: str | None = None) -> list:
    """
    Scan and connect to all available RD3005 / KA3005 power supplies.

    Parameters
    ----------
    resource : str | None
        Optional COM port or VISA resource string to connect to a specific device.

    Returns
    -------
    list[RD3005]
        List of connected power supply instances.
    """
    from Instruments_Libraries.RD3005 import RD3005
    import serial.tools.list_ports
    import logging

    logger = logging.getLogger(__name__)
    connected_devices = []

    target_ids = ["KORAD", "RND 320-KA3005P"]

    # If a specific resource is provided
    if resource:
        logger.info(f"Using provided resource: {resource}")
        connected_devices.append(RD3005(resource))
        return connected_devices

    # Otherwise, scan all COM ports
    ports = serial.tools.list_ports.comports()
    filtered_ports = [p for p in ports if "bluetooth" not in p.description.lower()]
    filtered_ports.sort(key=lambda p: (0 if "rd3005" in p.description.lower() or "ka3005" in p.description.lower() else 1, p.device))
    logger.info(f"Filtered COM ports: {[p.device for p in filtered_ports]}")

    for port in filtered_ports:
        inst = None
        try:
            logger.info(f"Trying port {port.device} ({port.description})")
            inst = RD3005(port.device)
            idn = inst.get_idn()
            if idn and any(tid in idn for tid in target_ids):
                logger.info(f"Power supply found on {port.device}: {idn}")
                connected_devices.append(inst)
            else:
                inst.close()
        except Exception as e:
            logger.warning(f"Error connecting to {port.device}: {e}")
            if inst:
                try:
                    inst.close()
                except Exception:
                    pass
            continue

    if not connected_devices:
        raise RuntimeError("No suitable power supply found.")

    return connected_devices

def PowerMeter(index: int = 0, resource: str | None = None) -> PM100D:  # noqa: N802
    """
    Auto-detect a connected Thorlabs PM100-series power meter.
    """
    from Instruments_Libraries.PM100D import PM100D

    if resource:
        return PM100D(resource)

    # Use auto-discovery logic similar to finding all PM100s and picking by index
    rm = visa.ResourceManager()
    matches = []

    try:
        resources = rm.list_resources("?*::INSTR")
    except ValueError:
        resources = []

    for res in resources:
        if "USB" not in res:
            continue  # PM100 is typically USB
        try:
            with rm.open_resource(res) as inst:
                inst.timeout = 200
                idn = None
                try:
                    query_func = getattr(inst, "query", None)
                    if callable(query_func):  # Check if it supports query
                        try:
                            idn = query_func("*IDN?").strip()
                        except Exception:
                            pass

                    if idn is None:
                        write_func = getattr(inst, "write", None)
                        read_func = getattr(inst, "read", None)
                        if callable(write_func) and callable(read_func):  # Fallback to write/read
                            try:
                                write_func("*IDN?")
                                idn = read_func().strip()
                            except Exception:
                                pass
                except Exception:
                    pass

                if idn and "PM100" in idn:
                    matches.append(res)
        except Exception:
            continue

    if not matches:
        raise RuntimeError("No Thorlabs PM100-series power meter found.")

    if not (0 <= index < len(matches)):
        raise IndexError(f"index {index} out of range (found {len(matches)} device(s)).")

    return PM100D(matches[index])


def LU1000(resource: str | None = "USB") -> LU1000_Cband:  # noqa: N802
    from Instruments_Libraries.LU1000 import LU1000_Cband
    if resource is None:
        resource = "USB"
    return LU1000_Cband(resource)
    



def SpecAnalyser(resource: str | None = None) -> MS2760A:  # noqa: N802
    from Instruments_Libraries.MS2760A import MS2760A

    # Defaults to localhost per user request for hardcoded localhost
    if resource is None:
        resource = "127.0.0.1"
    return MS2760A(resource)

def SigGen(resource: str | None = None, visa_library: str = "@ivi") -> MG3694C:
    from Instruments_Libraries.MG3694C import MG3694C

    if resource is None:
        try:
            # Try auto-discovery
            resource = find_resource(r"MG369")
            if resource is None:
                # fallback to the IP discovered on the network
                resource = "TCPIP0::169.254.236.243::INSTR"
                print(f"MG3694C not found by auto-discovery, using fallback IP {resource}")
        except RuntimeError:
            resource = "TCPIP0::169.254.236.243::INSTR"
            print(f"MG3694C not found by auto-discovery, using fallback IP {resource}")

    return MG3694C(resource_str=resource, visa_library=visa_library)


def RnS_SMA100B(resource: str | None = None, visa_library: str = "@ivi") -> SMA100B:  # noqa: N802
    from Instruments_Libraries.SMA100B import SMA100B

    if resource is None:
        resource = find_resource(r"SMA100B")
    return SMA100B(resource_str=resource, visa_library=visa_library)

def VNA(resource: str | None = None) -> MS4647B:  # noqa: N802
    from Instruments_Libraries.MS4647B import MS4647B

    if resource:
        return MS4647B(resource)

    # Try auto-discovery first
    try:
        resource = find_resource(r"MS4647B")
        return MS4647B(resource)
    except RuntimeError:
        # Auto-discovery failed, scan all TCPIP resources
        rm = visa.ResourceManager()
        for res in rm.list_resources():
            if "TCPIP" in res:
                try:
                    return MS4647B(res)
                except Exception:
                    continue
        # Fallback to hardcoded IP
        fallback = "TCPIP0::169.254.80.88::INSTR"
        return MS4647B(fallback)


def PhaseNoiseAnalyzer_APPH(resource: str | None = None) -> APPH:  # noqa: N802
    from Instruments_Libraries.APPH import APPH

    if resource is None:
        # Original logic looked for 'USB0'
        # We can try find_resource with regex
        try:
            resource = find_resource(r"APPH")
        except RuntimeError:
            # Fallback to finding any USB0
            rm = visa.ResourceManager()
            for res in rm.list_resources():
                if res.startswith("USB0"):
                    resource = res
                    break

    if resource is None:
        raise RuntimeError("APPH not found.")

    return APPH(resource)

def PowerSupply_GPP4323(resource: str | None = None) -> GPP4323:
    """
    Scan and connect to the first available GW-Instek GPP-4323 power supply.

    Parameters
    ----------
    resource : str | None
        Optional COM port or VISA resource string to connect to a specific device.

    Returns
    -------
    GPP4323
        Connected GPP4323 instance.
    """
    import serial.tools.list_ports
    import re
    import logging
    from Instruments_Libraries.GPP4323 import GPP4323
    from Instruments_Libraries.BaseInstrument import BaseInstrument

    logger = logging.getLogger(__name__)

    # If a resource was explicitly provided, connect directly
    if resource:
        if resource.upper().startswith("COM"):
            resource = BaseInstrument.com_to_asrl(resource)
        logger.info(f"Using provided resource: {resource}")
        return GPP4323(resource)

    # Regex to match the GPP4323 ID
    serial_regex = r'^GW INSTEK,GPP-4323.*'

    # List all COM ports
    ports = list(serial.tools.list_ports.comports())

    # Filter out Bluetooth devices
    filtered_ports = [port for port in ports if "bluetooth" not in port.description.lower()]

    # Sort ports so "gpp" in description is prioritized
    filtered_ports.sort(key=lambda port: (0 if "gpp" in port.description.lower() else 1, port.device))

    logger.info(f"Filtered COM ports: {[p.device for p in filtered_ports]}")

    selected_port = None
    GPP = None

    # Iterate over filtered COM ports
    for port in filtered_ports:
        try:
            logger.info(f"Trying port {port.device} ({port.description})")
            resource_str = BaseInstrument.com_to_asrl(port.device)
            GPP = GPP4323(resource_str)
            idn = GPP.get_idn()
            if re.match(serial_regex, idn.upper()):
                logger.info(f"GPP4323 found on {port.device}: {idn}")
                selected_port = port.device
                break  # stop at first matching device
            else:
                GPP.close()
        except Exception as e:
            logger.warning(f"Error connecting to {port.device}: {e}")
            if GPP:
                try:
                    GPP.close()
                except Exception:
                    pass
            continue

    if selected_port is None:
        raise RuntimeError("No suitable GPP4323 Power Supply found.")

    # Return the connected instance
    return GPP
    

def UXR_1002A(resource: str | None = None) -> UXR:  # noqa: N802
    from Instruments_Libraries.UXR import UXR

    if resource is None:
        # Keep original hardcoded fallback
        resource = "TCPIP0::KEYSIGH-Q75EBO9.local::hislip0::INSTR"

    my_UXR = UXR(resource)  # noqa: N806
    # Preservation of original init settings logic
    # Note: exception handling is now up to caller or BaseInstrument
    try:
        my_UXR.system_header("off")
        my_UXR.waveform_byteorder("LSBFirst")
        my_UXR.waveform_format("WORD")
        my_UXR.waveform_streaming("off")
    except Exception as e:
        logger.warning(f"Failed to set initial UXR settings: {e}")

    return my_UXR


def RnS_FSWP50(resource: str | None = None) -> FSWP50:  # noqa: N802
    from Instruments_Libraries.FSWP50 import FSWP50

    if resource is None:
        # Original hardcoded IP
        resource = "169.254.253.126"
    return FSWP50(resource)


# =============================================================================
# Main Factory / Selector
# =============================================================================


def InstInit(num) -> typing.Any:  # noqa: N802
    """
    Initialize instrument based on selection string.
    Recommended to use specific functions (e.g. SpecAnalyser()) directly instead.
    """
    map_func = {
        " Anrtisu Spectrum Analyzer MS2760A  ": SpecAnalyser,
        " Anritsu Signal Generator MG3694C  ": SigGen,
        " Anritsu Vectro Analyzer MS4647B  ": VNA,
        " Power Meter ThorLabs PM100D  ": PowerMeter,
        " Novoptel Laser LU1000  ": LU1000,
        " Yokogawa Optical Spectrum Analyzer AQ6370D  ": OSA,
        " KEITHLEY Source Meter 2612  ": SourceMeter,
        " Power Supply KA3005 ": PowerSupply,
        " CoBrite Tunable Laser  ": Laser_CoBrite,
        " AnaPico AG,APPH20G  ": PhaseNoiseAnalyzer_APPH,
        " 4-Channels Power Suppy GPP4323 ": PowerSupply_GPP4323,
        " Rohde and Schwarz SMA100B  ": RnS_SMA100B,
        " Keysight UXR0702A  ": UXR_1002A,
        " Rohde and Schwarz FSWP50  ": RnS_FSWP50,
    }

    func = map_func.get(num)
    if func:
        return func()
    else:
        raise ValueError("Invalid Instrument Selected")

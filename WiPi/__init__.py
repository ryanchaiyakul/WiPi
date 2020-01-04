import sys
from . import linux, win32, wifi

def getWifi(interface:str)->wifi.Wifi:
        if sys.platform == "linux":
            return linux._LinuxWifi(interface)
        return win32._WinWifi(interface)

def getAccessPoint(interface:str)->linux._LinuxAccessPoint:
    if sys.platform == "linux":
        return linux._LinuxAccessPoint(interface)
    return None

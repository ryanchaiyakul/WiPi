import sys
from . import linux, win32, wifi, access_point

def getWifi(interface:str)->wifi.Wifi:
        if sys.platform == "linux":
            return linux._WifiLinux(interface)
        return win32._WifiWin(interface)

def getAccessPoint(interface:str)->access_point.AccessPoint:
    if sys.platform == "linux":
        return access_point.AccessPoint(interface)
    return None

import sys
from . import linux, win32

def getWifi(interface:str)->wifi.Wifi:
        if sys.platform == "linux":
            return linux.WifiLinux(interface)
        return win32.WifiWin(interface)

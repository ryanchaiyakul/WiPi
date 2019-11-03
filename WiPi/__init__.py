import sys
from . import linux, win32

def getWifi(interface:str)->wifi.Wifi:
        if sys.platform == "linux":
            return linux._WifiLinux(interface)
        return win32._WifiWin(interface)

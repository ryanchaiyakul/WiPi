from . import linux, win64

def getWifi(interface:str)->Wifi:
        if sys.platform == "linux":
            return linux.WifiLinux(interface)
        return win64.WifiWin(interface)

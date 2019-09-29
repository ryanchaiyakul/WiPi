import subprocess

from . import constants, wifi

# Local Constants
BINPATH = constants.BINPATH / "win32"

class WifiWin(wifi.Wifi):

    def scan_ssid(self)->bool:
        super().scan_ssid()
        clean = subprocess.run(
            ["sh", str(BINPATH.joinpath("scan"))], stdout=subprocess.PIPE).stdout.decode('utf-8')

        # Parse stdout
        i = 0
        while True:
            i += 1
            index = clean.find("SSID {} : ".format(i))
            if index == -1:
                break
            clean = clean[index+9:]
            ssid = clean[:clean.find('\r')]
            if ssid != "":
                self._logger.debug("ssid: {} found".format(ssid))
                self._ssid_list.append(ssid)
        return self.scan_ssid_helper()
    
    def connect(self, ssid: str, passwd: str, country: str, hidden_network: bool):
        pass

    def update_status(self):
        pass

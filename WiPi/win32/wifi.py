import subprocess

from .. import constants, wifi

# Local Constants
BINPATH = constants.PATH.BIN / "win32"


class Wifi(wifi.Wifi):
    """wifi class that utilizes commands built into Windows

    NOT COMPLETE
    """

    def scan_ssid(self)->bool:
        """refreshes ssid_list with seeable networks

        Returns:
            bool -- T/F = Worked/Failed
        """
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

    #! function signature needed to satisfy abstract class
    # TODO not a priority but would be a goal
    def connect(self, ssid: str, passwd: str, country: str, hidden_network: bool):
        pass

    #! function signature needed to satisfy abstract class
    # TODO not a priority but would be a goal
    def update_status(self):
        pass

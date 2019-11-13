import subprocess

from . import wifi, constants

# Local Constants
BINPATH = constants.BINPATH / "linux"


class _WifiLinux(wifi.Wifi):
    """wifi class that utilizes commands built into Linux

    - iwconfig
    - ifconfig
    - iwlist
    """

    @property
    def status(self)->dict:
        """status of the interface
        
        Returns:
            dict -- interface status as a dictionary
        """
        ret = super().status
        ret = {"name": self.interface, "network": self._network_status,
               "interface": self._interface_status}
        # If interface is connected to a network
        if ret["network"] == constants.ONLINE:
            ret = {**ret, 'ssid': self._ssid, 'frequency': self._frequency}
        return ret

    def update_status(self):
        """API function that calls private functions to refresh the status
        """
        if super().update_status():
            self._status_interface()
            self._status_network()

    def _status_interface(self):
        """updates interface status
        """
        self._logger.info(
            "checking interface {} status".format(self.interface))
        raw = subprocess.run(["bash", BINPATH.joinpath(
            "status"), self.interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        err = raw.stderr.decode('utf-8')
        stdout = raw.stdout.decode('utf-8').replace("\n", "")

        self._logger.debug("stdout : {}  \nstder : {}".format(stdout, err))

        # Get status
        status = constants.OFFLINE
        if err != "":
            self._logger.error(
                "interface {} status is unknown".format(self.interface))
            self._logger.error("traceback : \n {}".format(err))
            status = constants.UNKNOWN
        elif stdout == "0x1003":
            self._logger.info(
                "interface {} is set to 'up'".format(self.interface))
            status = constants.ONLINE
        else:
            self._logger.warning(
                "interface {} is set to 'down'".format(self.interface))

        self._interface_status = status

    def _status_network(self):
        """updates network status
        """
        self._logger.info(
            "checking interface {} network connections".format(self.interface))
        raw = subprocess.run(["bash", BINPATH.joinpath(
            "network")], stdout=subprocess.PIPE).stdout.decode('utf-8')
        self._logger.debug("stdout : \n{}".format(raw))

        # Decode raw stdout
        device_list = raw.split("\n")

        device_dict = {}
        for pair in device_list:
            if pair != "":
                key_val = pair.split(":")
                device_dict[key_val[0]] = key_val[1]
        self._logger.debug("interface list {}".format(device_dict))

        # Get status
        status = constants.OFFLINE
        if self.interface not in device_dict:
            self._logger.error(
                "interface {} network status is unknown".format(self.interface))
            status = status = constants.UNKNOWN
        elif device_dict[self.interface] == " up":
            status = constants.ONLINE
            self._logger.info(
                "interface {} is connected to a network".format(self.interface))

            # Checks for ssid and frequency if connected
            self._linux_status_network_helper()
        else:
            self._logger.warning(
                "interface {} is not connected to a network".format(self.interface))

        self._network_status = status

    def _linux_status_network_helper(self):
        """helper function to update network status
        """
        raw = subprocess.run(["bash", BINPATH.joinpath(
            "iwconfig"), self.interface], stdout=subprocess.PIPE).stdout.decode('utf-8')

        raw = raw[raw.find("ESSID")+7:]
        self._ssid = raw[:raw.find('"')]
        raw = raw[raw.find("Frequency")+10:]
        self._frequency = raw[:raw.find("GHz")-1]
        self._logger.info("ssid : {}, frequency : {}".format(
            self._ssid, self._frequency))

    @property
    def interface(self)->str:
        """necessary for the setter
        
        Returns:
            str -- the name of the interface
        """
        return super().interface

    @interface.setter
    def interface(self, interface: str):
        """setter for interface
        
        Arguments:
            interface {str} -- the name of the interface
        """
        self._interface = interface
        self._validate_interface()

    def _set_interface(self, status: bool):
        """sets the interface to on or off
        
        Arguments:
            status {bool} -- True:on, False:off
        """
        # Convert status to str
        setting = "down"
        if status:
            setting = "up"

        self._logger.debug("setting device {} to {}".format(
            self, self.interface, setting))
        subprocess.run(["bash", BINPATH.joinpath(
            "set"), self.interface, setting])

    def _validate_interface(self):
        """Tests interface and sets it to None if it fails
        """
        # Update status information
        self.update_status()

        # Determine interface validity through status code
        if self.status["interface"] == 0:
            self._logger.info(
                "interface {} is already online".format(self.interface))
        elif self.status["interface"] == 1:
            # Automatically try to bring the interface online
            self._logger.warning(
                "interface {} is down. Trying to set to up".format(self.interface))
            self._set_interface(True)

            # Update status information again
            self.update_status()

            # Check if interface is online
            if self.status["interface"] != 0:
                self._logger.error(
                    "interface {} could not be brought up".format(self.interface))
                self._interface = None
                return
            self._logger.info(
                "interface {} successfully brought up".format(self.interface))
        elif self.status["interface"] == 2:
            self._logger.error(
                "interface {} status is unknown".format(self.interface))
            self._interface = None

        else:
            self._logger.error("unknown interface status : {}".format(
                self.status["interface"]))
            self._interface = None

    def connect(self, ssid: str, passwd: str, **kwargs)->bool:
        """connects to a WPA network
        
        Arguments:
            ssid {str} -- ssid of network
            passwd {str} -- password for network
        
        Keyword Arguements:
            country {str} -- country code https://www.iso.org/obp/ui/#search
            hidden_network {bool} -- True:is hdden, False:is not hidden
        
        Returns:
            bool -- True:connected, False:failed connecting
        """
        if super().connect(ssid, passwd):
            self._connect(ssid, passwd, kwargs.get(
                "country", "US"), kwargs.get("hidden_network", False))
        return self.connect_helper()

    def _connect(self, ssid: str, passwd: str, country: str, hidden_network: bool):
        """private function that connect calls.

        DO NOT CALL INDEPENDENTLY
        
        Arguments:
            ssid {str} -- ssid of network
            passwd {str} -- password for network
            country {str} -- country code https://www.iso.org/obp/ui/#search
            hidden_network {bool} -- True:is hdden, False:is not hidden
        """
        if self.status["interface"] != 0:
            self._logger.error(
                "interface {} is 'down' or unknown".format(self.interface))
            return

        if self.status["network"] == 0:
            self._logger.warning(
                "Currently connected to a network {}".format(self.status["ssid"]))

        wpa_string = self._wpa_passphrase(
            ssid, passwd, country, hidden_network)
        self._wpa_supplicant(wpa_string)

    def _wpa_passphrase(self, ssid: str, passwd: str, country: str, hidden_network: bool)->str:
        """creates a wpa_supplicant.conf file as a string
        
        Arguments:
            ssid {str} -- ssid of network
            passwd {str} -- password for network
            country {str} -- country code https://www.iso.org/obp/ui/#search
            hidden_network {bool} -- True:is hdden, False:is not hidden
        
        Returns:
            str -- generated wpa_supplicant.conf as a string
        """
        raw = subprocess.run(["bash", BINPATH.joinpath(
            "wpa_passphrase"), ssid, passwd], stdout=subprocess.PIPE).stdout.decode('utf-8')

        # Remove string psk
        clean = raw[:raw.find("#")]+raw[raw.find("\n", raw.find("#"))+2:]

        # Prepend network information
        clean = "country={}\n\n".format(country) + clean

        self._logger.info("Country Code : {}".format(country))

        # Hidden network
        if hidden_network:
            self._logger.info("hidden network setting requested")
            clean = clean[:len(clean)-2]
            clean += "\n    scan_ssid = 1\n}"

        return clean

    def _wpa_supplicant(self, config: str):
        """loads the wpa_supplicant.conf string
        
        Arguments:
            config {str} -- the wpa_supplicant.conf file as a string
        """
        self._logger.debug("config : \n{}".format(config))

        raw = subprocess.run(["bash", BINPATH.joinpath(
            "wpa_supplicant"), self.interface, config])

    def scan_ssid(self)->bool:
        """refreshes ssid_list with seeable networks
        
        Returns:
            bool -- T/F = Worked/Failed
        """
        if super().scan_ssid():
            if self.interface == "":
                self._logger.error(
                    "Can not scan for networks without an interface")
                return False

            raw = subprocess.Popen(['sudo', BINPATH.joinpath("scan"), self.interface],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Check for errors
            err = raw.stderr.read().decode('utf-8')
            if err != "":
                self._logger.error(
                    "traceback: {}".format(err.replace('\n', '')))  # Get rid of extra new lines
                return False

            clean = raw.stdout.read().decode('utf-8')

            # Parse stdout
            while True:
                index = clean.find("ESSID")
                if index == -1:
                    break
                clean = clean[index+7:]
                ssid = clean[:clean.find('"')]
                if ssid != "":
                    self._logger.debug("ssid: {} found".format(ssid))
                    self._ssid_list.append(ssid)
            return self.scan_ssid_helper()

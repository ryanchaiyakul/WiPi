import abc
import logging
import pathlib
import subprocess

import Safe_Open

from . import interface, constants


BINPATH = constants.PATH.BIN / "linux/access_point"


class AccessPoint(interface.Interface, metaclass=abc.ABCMeta):

    def __init__(self, interface: str = ""):
        super().__init__(interface=interface)
        self._logger = logging.getLogger(__name__)

        self._service_status = {constants.SERVICE.HOSTAPD: constants.SERVICE.STATUS.INACTIVE,
                                constants.SERVICE.DNSMASQ: constants.SERVICE.STATUS.INACTIVE, constants.SERVICE.DHCPCD: constants.SERVICE.STATUS.INACTIVE}

    def _get_status(self)->dict:
        if not hasattr(self, "_service_status"):
            return super()._get_status()
        return self._service_status

    def update_status(self):
        for v in constants.SERVICE:

            if type(v).__name__ != type(constants.SERVICE.STATUS).__name__:

                if v not in self._service_status.keys():
                    self._logger.error("Unknown service {}".format(v))
                    return

                clean = subprocess.run(["bash", BINPATH.joinpath(
                    "status"), v], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')

                status = None

                if clean.find("active"):
                    status = constants.SERVICE.STATUS.ACTIVE
                elif clean.find("inactive"):
                    status = constants.SERVICE.STATUS.INACTIVE
                elif clean.find("failed"):
                    status = constants.SERVICE.STATUS.FAILED

                if status is None:
                    self._logger.warning("Unknown status: {}".format(clean))
                    return
                else:
                    self._logger.info("{} is {}".format(v, status))

                self._service_status[v] = status
            
            else:
                self._logger.debug("Filtering out status from constants")

    def set_dhcpcd(self):
        if hasattr(self, "_dhcpcd"):
            config = self._dhcpcd
        else:
            config = self.get_dhcpcd()

        self._logger.debug("config : {}".format(config))
        if config != "":
            with Safe_Open.Backup(constants.PATH.DHCPCD, AccessPoint._check_dhcpcd) as dhcpcd:
                with dhcpcd.open('r') as stream:
                    if stream.read().find(config) != -1:
                        self._logger.info("dhcpcd has already been set")
                        return
                    self._logger.info("dhcpcd has not been set")

                with dhcpcd.open('a') as stream:
                    stream.write(config)
            return

        self._logger.error("interface is not set")

    @staticmethod
    def _check_dhcpcd(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("dhcpcd")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""

    def get_dhcpcd(self):
        if self.interface == "":
            return ""

        return "interface {}\n" \
        "static ip_address=192.168.4.1/24\n" \
        "nohook wpa_supplicant".format(self.interface)

    def set_dnsmasq(self):
        if hasattr(self, "_dnsmasq"):
            config = self._dnsmasq
        else:
            config = self.get_dnsmasq()

        if config != "":
            with Safe_Open.Backup(constants.PATH.DNSMASQ, AccessPoint._check_dnsmasq) as dnsmasq:
                with dnsmasq.open('r') as stream:
                    if stream.read().find(config) != -1:
                        self._logger.info("dnsmasq has already been set")
                        return
                    self._logger.info("dnsmasq has not been set")

                with dnsmasq.open('w') as stream:
                    stream.write(config)
            return

        self._logger.error("interface is not set")

    @staticmethod
    def _check_dnsmasq(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("dnsmasq")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""

    def get_dnsmasq(self):
        if self.interface == "":
            return ""

        return "interface={}      # Use the require wireless interface - usually wlan0\n" \
        "dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h".format(self.interface)

    def set_hostapd(self):
        if hasattr(self, "_hostapd"):
            config = self._hostapd
        else:
            return

        if config != "":
            with Safe_Open.Backup(constants.PATH.HOSTAPD.LOCAL, AccessPoint._check_hostapd) as hostapd:
                with hostapd.open('r') as stream:
                    if stream.read().find(config) != -1:
                        self._logger.info("hostapd has already been set")
                        return
                    self._logger.info("hostapd has not been set")

                with hostapd.open('w') as stream:
                    stream.write(config)

            with Safe_Open.Backup(constants.PATH.HOSTAPD.ABS, AccessPoint._check_hostapd) as hostapd:
                with hostapd.open('r') as stream:
                    if stream.read().find(config) != -1:
                        self._logger.info("hostapd has already been set")
                        return
                    self._logger.info("hostapd has not been set")

                with hostapd.open('w') as stream:
                    hostapd.write("\n" + APPEND_STRING)
            return

        self._logger.error("interface is not set")

    @staticmethod
    def _check_hostapd(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("hostapd")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""

    def get_hostapd(self, ssid: str, passwd: str = "", hw_mode: str = "g", channel: int = 0):
        if self.interface == "":
            return ""

        return "interface={}\n" \
        "driver=nl80211\n" \
        "ssid={}\n" \
        "hw_mode={}\n" \
        "channel={}\n" \
        "wmm_enabled=0\n" \
        "macaddr_acl=0\n" \
        "auth_algs=1\n" \
        "ignore_broadcast_ssid=0\n" \
        "wpa=2\n" \
        "wpa_passphrase={}\n" \
        "wpa_key_mgmt=WPA-PSK\n" \
        "wpa_pairwise=TKIP\n" \
        "rsn_pairwise=CCMP".format(self.interface, ssid, hw_mode, channel, passwd)

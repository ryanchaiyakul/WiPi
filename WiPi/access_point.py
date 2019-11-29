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

    def _get_status(self)->dict:
        return super()._get_status()

    def update_status(self):
        pass
    
    def set_dhcpcd(self):
        self._logger.info("setting dhcpcd")
        config = self._get_dhcpcd()

        self._logger.debug("config : {}".format(config))
        if config != "":
            with Safe_Open.Backup(constants.PATH.DHCPCD, AccessPoint._check_dhcpcd) as dhcpcd:
                pass
                #with dhcpcd.open('a') as stream:
                    #pass
                    #stream.write(config)
            return
        self._logger.error("interface is not set")
    
    @staticmethod
    def _check_dhcpcd(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("dhcpcd")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""

    def _get_dhcpcd(self):
        if self.interface == "":
            return ""

        return """interface {}
            static ip_address=192.168.4.1/24
            nohook wpa_supplicant""".format(self.interface)

    def set_dnsmasq(self):
        config = self._get_dnsmasq()
        if config != "":
            with Safe_Open.Backup(constants.PATH.DNSMASQ, AccessPoint._check_dnsmasq) as dnsmasq:
                with dnsmasq.open('w') as stream:
                    stream.write(config)
        self._logger.error("interface is not set")

    @staticmethod
    def _check_dnsmasq(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("dnsmasq")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""

    def _get_dnsmasq(self):
        if self.interface == "":
            return ""

        return """interface={}      # Use the require wireless interface - usually wlan0
        dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h""".format(self.interface)

    def set_hostapd(self):
        config = self._get_hostapd()
        if config != "":
            with Safe_Open.Backup(constants.PATH.HOSTAPD.LOCAL, AccessPoint._check_hostapd) as hostapd:
                with hostapd.open('w') as stream:
                    stream.write(config)
            with Safe_Open.Backup(constants.PATH.HOSTAPD.ABS, AccessPoint._check_hostapd) as hostapd:
                with hostapd.open('r+') as stream:
                    APPEND_STRING = "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""
                    if stream.read().find(APPEND_STRING) == -1:
                        hostapd.write("\n" + APPEND_STRING)
        self._logger.error("interface is not set")

    def run(self):
        if self.interface == "":
            return
            
        self.set_dhcpcd()
        self.set_dnsmasq()
        self.set_hostapd()

    @staticmethod
    def _check_hostapd(file_path: pathlib.Path):
        return subprocess.run(["bash", BINPATH.joinpath("hostapd")], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8') != ""
    
    def _get_hostapd(self, ssid:str, passwd:str ="", hw_mode:str = "g", channel:int = 0):
        if self.interface == "":
            return ""
        
        return """interface={}
        driver=nl80211
        ssid={}
        hw_mode={}
        channel={}
        wmm_enabled=0
        macaddr_acl=0
        auth_algs=1
        ignore_broadcast_ssid=0
        wpa=2
        wpa_passphrase={}
        wpa_key_mgmt=WPA-PSK
        wpa_pairwise=TKIP
        rsn_pairwise=CCMP""".format(self.interface, ssid, hw_mode, channel, passwd)

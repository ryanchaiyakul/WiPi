import logging
import pathlib
import subprocess

from PyAccessPoint import pyaccesspoint

from .. import access_point, constants


BINPATH = constants.PATH.BIN / "linux/access_point"


class AccessPoint(access_point.AccessPoint):

    def __init__(self, interface: str = ""):
        """ Wrapper class of pyaccesspoint.AccessPoint to work with the WiPi accesspoint abc.

        Keyword Arguments:
            interface {str} -- unique interface designated to the AccessPoint (default: {""})
        """
        super().__init__(interface=interface)

        self._status = {constants.SERVICE.HOSTAPD: constants.SERVICE.STATUS.INACTIVE,
                        constants.SERVICE.DNSMASQ: constants.SERVICE.STATUS.INACTIVE,
                        constants.SERVICE.DHCPCD: constants.SERVICE.STATUS.INACTIVE,
                        constants.SERVICE.ACCESSPOINT: constants.SERVICE.STATUS.INACTIVE}

    def update_status(self):
        """updates self._status by running commandline commands.
        """
        for v in constants.SERVICE:
            if type(v).__name__ not in [type(constants.SERVICE.STATUS).__name__, type(constants.SERVICE.START)]:
                status = None

                if type(v).__name__ == type(constants.SERVICE.ACCESSPOINT).__name__:
                    if hasattr(self, "access_point"):
                        status = constants.STATUS.INACTIVE
                        if self.access_point.is_running():
                            status = constants.STATUS.ACTIVE
                    else:
                        status = constants.STATUS.FAILED
                else:
                    if v not in self._status.keys():
                        self._logger.error("Unknown service {}".format(v))
                        return

                    clean = subprocess.run(["bash", BINPATH.joinpath(
                        "status"), v], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')

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

                self._status[v] = status

            else:
                self._logger.debug("Filtering out status from constants")

    def start(self, inet=None, ip="192.168.4.1", netmask="255.255.255.0", ssid="MyAccessPoint", password="password"):
        """ Starts the accesspoint.
        """
        start_consts = constants.ACCESSPOINT.START

        if password == "password":
            self._logger.warning(
                "No password specified. Using default password: 'password'")

        self._logger.debug("ip : {}, ssid : {}, password : {}".format())

        self.access_point = pyaccesspoint.AccessPoint(
            wlan=self.interface, inet=inet, ip=ip, netmask=netmask, ssid=ssid, password=password)
        self.access_point.start()

    def stop(self):
        """ Stops the accesspoint.
        """
        if hasattr(self, access_point):
            self._logger.info("stopping accesspoint")
            self.access_point.stop()
        else:
            self._logger.error("accesspoint has not been started")

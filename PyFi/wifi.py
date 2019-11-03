import abc
import subprocess
import sys
import logging
import pathlib
import time
from typing import List

from . import constants


class Wifi(metaclass=abc.ABCMeta):
    """abstract class that establishes the necessary function signatures and properties for a wifi class.
    """

    def __init__(self, interface: str = ""):
        self._logger = logging.getLogger(__name__)

        if interface == "":
            self._logger.warning(
                "{}.interface not passed during initialization".format(self))
        self.interface = interface

    @property
    def status(self)->dict:
        """status is a read-only dictionary.
        contains information the interface itself and the connection

        Returns:
            dict -- returns an empty dictionary as default
        """
        return {}

    @abc.abstractmethod
    def update_status(self):
        """updates the private variables that status returns as a dictionary with keys
        """
        # Check if self.interface is not set
        if self.interface == "":
            self._logger.warning("{}.interface is not set".format(self))

            # No information can be gathered so set to unknown
            self._network_status = constants.UNKNOWN
            self._interface_status = constants.UNKNOWN
            return False
        return True

    @property
    def interface(self)->str:
        """a string that corresponds to the interface name

        Returns:
            string -- name of the interface (ex. wlan0). Defaults to "" if interface is None
        """
        if not hasattr(self, "_interface") or self._interface is None:
            self._logger.warning("{}.interface is not set".format(self))
            return ""
        return self._interface

    @interface.setter
    def interface(self, interface: str):
        """sets self._interface. Classes that extend are reccomended to add validity checks

        Arguments:
            interface {str} -- name of the interface
        """
        self._interface = interface

    @abc.abstractmethod
    def connect(self, ssid: str, passwd: str, **kwargs)->bool:
        """tries to establish a WPA connection to a network

        Arguments:
            ssid {str} -- name of the network
            passwd {str} -- WPA-PSK of the network

        Returns:
            bool -- T/F = Worked/Failed
        """
        self._logger.info(
            "trying to connect to network with ssid : {}".format(ssid))

        if self.interface == "":
            self._logger.error("{}.interface is not set".format(self))
            return False

        if self.status["interface"] != constants.ONLINE:
            self._logger.error("{}.interface is not ONLINE but is {}".format(
                self, self.status["interface"]))
            return False

        self.scan_ssid()
        if ssid not in self.ssid_list:
            self._logger.warning(
                "ssid not found in ssid list, might be a hidden network")
        self._logger.info("ssid {} found in network list".format(ssid))
        return True

    def connect_helper(self) -> bool:
        """assists connect function and serves as helper for classes that extend this base class

        Returns:
            bool -- T/F = Worked/Failed
        """
        for i in range(1, 6):
            time.sleep(5)
            self._logger.info("{}/5 tries for network confirmation".format(i))
            self.update_status()
            if self.status["network"] == 0:
                self._logger.info("successfully connected to {} with frequency of {} GHz".format(
                    self.status["ssid"], self.status["frequency"]))
                return True
        self._logger.error("failed connecting to {}".format(ssid))
        return False

    @property
    def ssid_list(self)->list:
        """returns a list of found ssids

        Returns:
            list -- defaults to [] if list does not exist
        """
        if hasattr(self, "_ssid_list"):
            return self._ssid_list
        return []

    @abc.abstractmethod
    def scan_ssid(self)->bool:
        """scans for seeable networks. Removes old networks from list

        Returns:
            bool -- T/F = Worked/Failed
        """
        self._logger.info("scanning for ssid of networks")

        # Reset self._ssid_list
        self._ssid_list = []

    def scan_ssid_helper(self)->bool:
        """assists scan_ssid function and serves as helper for classes that extend this base class

        Returns:
            bool -- T/F = Worked/Failed
        """
        # Handle new self._ssid_list
        if self._ssid_list == []:
            self._logger.error("no ssids found")
            return False
        self._logger.info("ssids: {} found".format(self._ssid_list))
        return True

import abc
import sys
import logging
import subprocess

from . import constants


class Interface(metaclass=abc.ABCMeta):
    """abstract class that establishes the necessary function signatures and properties for an interface.
   
        Interface is the abstract base class of both Wifi and AccessPoint as they extend the functionality of a wlan interface.
    """

    VALID_INTERFACES = []       # Interfaces that exist of the host machine
    if sys.platform == "linux":
        clean = subprocess.run(["bash", constants.PATH.BIN.joinpath("linux/iw_interface")], stdout=subprocess.PIPE).stdout.decode('utf-8')

        sep_string =clean.split("\n")
        for v in sep_string:
            VALID_INTERFACES.append(v[11:])

    TAKEN_INTERFACES = []       # Interfaces taken by Interface objects

    def __init__(self, interface: str = ""):
        self._logger = logging.getLogger(__name__)

        if interface == "":
            self._logger.warning(
                "{}.interface not passed during initialization".format(self))
        self.interface = interface

    def _get_status(self)->dict:
        """status is a read-only dictionary.
        Override self._status to change the returned status.

        Returns:
            dict -- returns an empty dictionary as default
        """
        if hasattr(self, "_status"):
            return self._status
        return {}

    status = property(fget=lambda self: self._get_status())

    @abc.abstractmethod
    def update_status(self):
        """updates the private variables that status returns as a dictionary with keys
        """
        # Check if self.interface is not set
        if self.interface == "":
            self._logger.warning("{}.interface is not set".format(self))
            return False
        return True

    def _get_interface(self)->str:
        """a string that corresponds to the interface name

        Returns:
            string -- name of the interface (ex. wlan0). Defaults to "" if interface is None
        """
        if not hasattr(self, "_interface") or self._interface is None:
            self._logger.warning("{}.interface is not set".format(self))
            return ""
        return self._interface

    def _set_interface(self, interface: str):
        """sets self._interface. Classes that extend are recomended to add validity checks

        Arguments:
            interface {str} -- name of the interface
        """
        self._interface = None
        
        if Interface.VALID_INTERFACES == []:
            self._logger.warning("Valid interfaces were not found. Cannot determine validity")
        elif interface not in Interface.VALID_INTERFACES:
            self._logger.error("{} is not a valid interface. Valid Interfaces : {}".format(interface, Interface.VALID_INTERFACES))
            return
        
        if interface in Interface.TAKEN_INTERFACES:
            self._logger.error("{} is already taken".format(interface))
            return

        if hasattr(self, "_interface") and self._interface in Interface.TAKEN_INTERFACES:
            self._logger.info("switching from {} to {}".format(self._interface, interface))
            Interface.TAKEN_INTERFACES.remove(self._interface)
        
        self._interface = interface

    interface = property(fget=lambda self: self._get_interface(),
                         fset=lambda self, value: self._set_interface(value))

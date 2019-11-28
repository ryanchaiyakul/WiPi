import abc
import sys
import logging

from . import constants


class Interface(metaclass=abc.ABCMeta):
    """abstract class that establishes the necessary function signatures and properties for an interface.
   
        Interface is the abstract base class of both Wifi and AccessPoint as they extend the functionality of a wlan interface.
    """

    VALID_INTERFACES = []
    if sys.platform == "linux":
        pass

    TAKEN_INTERFACES = []

    def __init__(self, interface: str = ""):
        self._logger = logging.getLogger(__name__)

        if interface == "":
            self._logger.warning(
                "{}.interface not passed during initialization".format(self))
        self.interface = interface

    @abc.abstractproperty
    def _get_status(self)->dict:
        """status is a read-only dictionary.
        Overide this property in order to provide the necessary status information.

        Returns:
            dict -- returns an empty dictionary as default
        """
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
        self._interface = interface

    interface = property(fget=lambda self: self._get_interface(),
                         fset=lambda self, value: self._set_interface(interface))

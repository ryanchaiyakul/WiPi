import abc
import time

from . import interface, constants

class AccessPoint(interface.Interface, metaclass=abc.ABCMeta):

    def __init__(self, interface: str = ""):
        self._service_status = {constants.SERVICE.HOSTAPD: constants.SERVICE.STATUS.INACTIVE,
                                constants.SERVICE.DNSMASQ: constants.SERVICE.STATUS.INACTIVE, constants.SERVICE.DHCPCD: constants.SERVICE.STATUS.INACTIVE}

    @abc.abstractmethod
    def start(self):
        pass
    
    @abc.abstractmethod
    def stop(self):
        pass

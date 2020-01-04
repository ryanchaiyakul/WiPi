import abc
import time

from . import interface, constants

class AccessPoint(interface.Interface, metaclass=abc.ABCMeta):

    def __init__(self, interface: str = ""):
        super().__init__(interface=interface)

    @abc.abstractmethod
    def start(self):
        pass
    
    @abc.abstractmethod
    def stop(self):
        pass

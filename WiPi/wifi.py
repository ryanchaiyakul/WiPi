import abc
import collections

from . import interface


class Wifi(interface.Interface):

    @abc.abstractmethod
    def connect(self, ssid: str, password: str = "", hidden_network: bool = False):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass
import abc
from WiPi import interface


class Wifi(interface.Interface):

    @abc.abstractmethod
    def connect(self, ssid: str, passwd: str = "", hidden_network: bool = False):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

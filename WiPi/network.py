import abc
import dataclasses
import typing

@dataclasses.dataclass
class Connection:
    interface: str
    bssid: str
    flags: dict

class BaseNetwork:
    _connection: Connection = Connection

@dataclasses.dataclass
class Network(BaseNetwork, metaclass=abc.ABCMeta):
    ssid: str
    password: str = ""
    hidden_network: bool = False

    @abc.abstractmethod
    def add_connection(self, interface: str):
        if interface in vars(self).keys():
            raise ValueError("{} already has a connection to this network".format(interface))
    
    @abc.abstractmethod
    def enable(self, interface: str):
        pass
    
    @abc.abstractmethod
    def disable(self, interface: str):
        pass

    def delete(self, interface: str):
        if interface not in vars(self).keys():
            raise ValueError("{} does not have a connection to this network".format(interface))
        
        delattr(self, interface)
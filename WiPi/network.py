import abc
import dataclasses
import typing


@dataclasses.dataclass
class Connection:
    interface: str
    bssid: str
    flags: dict

    @abc.abstractmethod
    def enable(self):
        pass

    @abc.abstractmethod
    def disable(self):
        pass


@dataclasses.dataclass
class Network(metaclass=abc.ABCMeta):
    ssid: str
    password: str = ""
    hidden_network: bool = False

    @abc.abstractmethod
    def add_connection(self, interface: str):
        if interface in vars(self).keys():
            raise ValueError(
                "{} already has a connection to this network".format(interface))

    def delete_connection(self, interface: str):
        if interface not in vars(self).keys():
            raise ValueError(
                "{} does not have a connection to this network".format(interface))

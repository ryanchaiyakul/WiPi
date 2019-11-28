import abc
import logging

from . import interface

class AccessPoint(interface.Interface, metaclass=abc.ABCMeta):

    def __init__(self, interface: str =""):
        super().__init__(interface=interface)
        self._logger = logging.getLogger(__name__)

    def status(self)->dict:
        pass

    def update_status(self):
        pass

    @property
    def interface(self)->str:
        return super().interface

    @interface.setter
    def interface(self, interface: str):
        super().interface = interface
import abc
import collections
import logging
import pathlib
import subprocess
import sys
import typing


def _run(fname: str, cmd_args: typing.List[str] = [], stdout: int = subprocess.DEVNULL, stderr: int = subprocess.DEVNULL) -> subprocess.CompletedProcess:
    """wraps subprocess call for easier use

    Arguments:
        fname {str} -- file name

    Keyword Arguments:
        cmd_args {typing.List[str]} -- commandline arguements (default: {[]})
        stdout {int} -- subprocess.PIPELINE (default: {subprocess.DEVNULL})
        stderr {int} -- subprocess.PIPELINE (default: {subprocess.DEVNULL})

    Returns:
        subprocess.CompletedProcess -- general output for both stdout and stderr parsing
    """
    fpath = pathlib.Path(__file__).parent.joinpath(
        "{}/{}/{}".format("bin", sys.platform, fname))
    return subprocess.run(['bash', fpath.as_uri(), *cmd_args], stdout=stdout, stderr=stderr)


def _get_interfaces() -> set:
    """returns avaliable interfaces as a set

    Returns:
        set -- can be empty if call fails
    """
    call = _run('get_interfaces', stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    # catches all errors
    if call.stderr.decode('utf-8') != "":
        return set()

    if sys.platform == "linux":
        return set(call.stdout.decode('utf-8')[22:-1].split('\n'))
    else:
        return set()


class Interface(metaclass=abc.ABCMeta):

    __interfaces = _get_interfaces()
    __taken_interfaces = set()

    def __init__(self, interface: str = ""):
        self.__logger = logging.getLogger(__file__)
        self.interface = interface

    def set_interface(self, interface: str):
        """ Do not override this function. Overide validate_interface to stop the setting if nececssary.
        """
        self.__logger.debug('setting {}.interface'.format(self))
        self._interface = ""    # Reset interface always

        if self.validate_interface(interface):
            self.__logger.info(
                '{}.interface set to: {}'.format(self, interface))
            type(self).__taken_interfaces.add(interface)
            self._interface = interface

    def validate_interface(self, interface: str) -> bool:
        """ Returns true if the passed interface is valid.
        """
        # Cannot check validity if information cannot be read
        if type(self).__interfaces == []:
            self.__logger.warning('Interfaces cannot be validated')
            return True

        # Interface does not exist
        if interface not in type(self).__interfaces:
            self.__logger.error(
                '{} is not a valid interface'.format(interface))
            return False
        # Interface is not unique
        if interface in type(self).__taken_interfaces:
            self.__logger.error('{} is already taken'.format(interface))
            return False
        return True

    def del_interface(self):
        """ Resets and frees the taken interface
        """
        if self._interface != "":
            self.__logger.info(
                'deleting {}.interface: {}'.format(self, self.interface))
            type(self).__taken_interfaces.remove(self.interface)

        self._interface = ""

    interface = property(fget=lambda self: self._interface,
                         fset=set_interface, fdel=del_interface)

    def _run(self, fname: str, cmd_args: typing.List[str] = [], stdout: int = subprocess.DEVNULL, stderr: int = subprocess.DEVNULL) -> typing.Union[subprocess.CompletedProcess,
                                                                                                                                                    None]:
        if self.interface != "":
            self.__logger.info(
                "running {} with args {}".format(fname, cmd_args))
            return _run(fname=fname, cmd_args=[self.interface], stdout=stdout, stderr=stderr)
        self.__logger.error("cannot run subproccess if interface is not set")
        return None

    @staticmethod
    def get_interfaces() -> set:
        return _get_interfaces()

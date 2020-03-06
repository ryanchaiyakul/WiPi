import subprocess
import collections
import typing

from WiPi import wifi, run


class Network:
    __networks: set

    def __init__(self, interface: str, network_id: int, ssid: str, bssid: str, flags: dict):
        self.interface = interface
        self.id = network_id
        self.ssid = ssid
        self.bssid = bssid
        self.flags = flags

    @classmethod
    def from_cli(cls, interface: str, line: str) -> 'Network':
        network_id, ssid, bssid, flags = line.split('\t')
        print(line)
        return cls(interface, network_id, ssid, bssid, flags)

    @classmethod
    def new(cls, interface:str, ssid: str, password: str = "", hidden_network: bool = False):
        scan_ssid = 0
        if hidden_network:
            scan_ssid = 1
        
        stdout = run(fname="{}/{}".format('network', 'add'),
                    cmd_args=[interface, '"{}"'.format(ssid), '"{}"'.format(password), str(scan_ssid)],
                    stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split('\n')

        network_id = stdout.pop(0)
        for error in stdout:
            if error != "OK":
                raise ValueError("failed creating a network")

        line = run(fname="{}/{}".format('network', 'status'),
                    cmd_args=[interface, network_id],
                    stdout=subprocess.PIPE).stdout.decode('utf-8')

        return cls.from_cli(interface=interface, line=line)

    def _run(self, fname: str, cmd_args: typing.List[str] = [], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) -> subprocess.CompletedProcess:
        return run(fname="{}/{}".format('network', fname),
                   cmd_args=[self.interface, self.id, *cmd_args],
                   stdout=stdout,
                   stderr=stderr)

    def enable(self, id: int) -> bool:
        call = self._run('enable', stdout=subprocess.PIPE)

        if call is None:
            return False

        if call.stdout.decode('utf-8') == "OK":
            return True
        return False

    def disable(self, id: int) -> bool:
        call = self._run('disable', stdout=subprocess.PIPE)

        if call is None:
            return False

        if call.stdout.decode('utf-8') == "OK":
            return True
        return False

    def delete(self):
        self._run(fname='delete')


class Wifi(wifi.Wifi):
    _network_status = collections.namedtuple(
        'network_status', ['id', 'ssid', 'bssid', 'flags'])

    def connect(self, ssid: str, password: str = "", hidden_network: bool = False):
        if self.interface == "":
            return False

        for network in self.networks:
            if ssid == network.ssid:
                pass
        else:
            pass

    def disconnect(self):
        if type(self.status) is type(self)._active_status:
            for network in self.networks:
                if network.flags.find('DISABLED') != -1:
                    pass

    @property
    def networks(self) -> set:
        call = self._run('get_networks', stdout=subprocess.PIPE)

        if call is None:
            return []

        ret = set()
        stdout = call.stdout.decode('utf-8')
        for line in stdout[stdout.find('\n')+1:-1].split('\n'):
            ret.add(Network.from_cli(interface=self.interface, line=line))

        return ret

    def update(self):
        call = self._run('get_status', stdout=subprocess.PIPE)

        if call is None:
            super().update()

        status = {}
        stdout = call.stdout.decode('utf-8')[:-1]
        for lines in stdout.split('\n'):
            key, value = lines.split('=')
            status[key] = value

        if 'ssid' in status.keys():
            self._status = type(self)._active_status(**status)
        else:
            self._status = type(self)._inactive_status(**status)

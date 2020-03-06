import subprocess

from WiPi import network, run

class Connection(network.Connection):
    network_id: int

class Network(network.Network):
    _connection = Connection

    def _run(self, fname: str, cmd_args: typing.List[str] = [], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) -> subprocess.CompletedProcess:
        return run(fname="{}/{}".format('network', fname),
                   cmd_args=[self.interface, self.id, *cmd_args],
                   stdout=stdout,
                   stderr=stderr)

    def add(self, interface:str):
        super().add(interface)

        scan_ssid = 0
        if self.hidden_network:
            scan_ssid = 1
        
        stdout = run(fname="{}/{}".format('network', 'add'),
                    cmd_args=[interface, '"{}"'.format(self.ssid), '"{}"'.format(self.password), str(scan_ssid)],
                    stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1].split('\n')

        network_id = stdout.pop(0)
        for error in stdout:
            if error != "OK":
                raise ValueError("failed creating a network")

        line = run(fname="{}/{}".format('network', 'status'),
                    cmd_args=[interface, network_id],
                    stdout=subprocess.PIPE).stdout.decode('utf-8')
        zip(type(self)._connection.__fields, line.split('\t'))
        network_id, ssid, bssid, flags = line.split('\t')
        setattr(self, interface, type(self)._connection(**line))

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
        super().delete()
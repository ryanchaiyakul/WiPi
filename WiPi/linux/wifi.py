from WiPi import wifi


class Wifi(wifi.Wifi):

    def connect(self, ssid: str, passwd: str = "", hidden_network: bool = False):
        pass

    def disconnect(self):
        pass

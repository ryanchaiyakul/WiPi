from WiPi.linux import wifi

a = wifi.Network.new('wlp2s0', 'RPiHosted', 'Snowy!!123')
print(a.ssid)
a.delete()
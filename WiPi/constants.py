import pathlib
import collections

# Path Constants

_path_key = ["BIN", "DHCPCD", "DNSMASQ",
             "HOSTAPD"]
_path_tuple = collections.namedtuple("path", _path_key)

_hostapd_key = ["LOCAL", "ABS"]
_hostapd_tuple = collections.namedtuple("hostapd", _hostapd_key)

_hostapd_local = pathlib.Path("/etc/hostapd/hostapd.conf")
_hostapd_abs = pathlib.Path("/etc/default/hostapd")

_hostapd = _hostapd_tuple(LOCAL=_hostapd_local, ABS=_hostapd_abs)

_bin = pathlib.Path(__file__).parent / "bin"
_dhcpcd = pathlib.Path("/etc/dhcpcd.conf")
_dnsmasq = pathlib.Path("/etc/dnsmasq.conf")

PATH = _path_tuple(BIN=_bin, DHCPCD=_dhcpcd, DNSMASQ=_dnsmasq, HOSTAPD=_hostapd)

# Network/Interface Status Codes
_status_key = ["ONLINE", "OFFLINE", "UNKNOWN"]

_status_tuple = collections.namedtuple("status", _net_key)

_online = 0x01
_offline = 0x02
_unknown = 0x03

STATUS = _status_tuple(ONLINE=_online, OFFLINE=_offline, UNKNOWN=_unknown)
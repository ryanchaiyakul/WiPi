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

_hostapd_path = _hostapd_tuple(LOCAL=_hostapd_local, ABS=_hostapd_abs)

_bin_path = pathlib.Path(__file__).parent / "bin"
_dhcpcd_path = pathlib.Path("/etc/dhcpcd.conf")
_dnsmasq_path = pathlib.Path("/etc/dnsmasq.conf")

PATH = _path_tuple(BIN=_bin_path, DHCPCD=_dhcpcd_path,
                   DNSMASQ=_dnsmasq_path, HOSTAPD=_hostapd_path)

# Wifi

_wifi_key = ["STATUS", "NETWORK", "INTERFACE", "FREQUENCY", "SSID"]
_wifi_tuple = collections.namedtuple("wifi", _wifi_key)

_wifi_network = "network"
_wifi_interface = "interface"
_wifi_frequency = "frequency"
_wifi_ssid = "ssid"

# Network/Interface Status Codes
_wifi_status_key = ["ONLINE", "OFFLINE", "UNKNOWN"]

_wifi_status_tuple = collections.namedtuple("wifi_status", _status_key)

_online = 0x01
_offline = 0x02
_unknown = 0x03

_wifi_status = _wifi_status_tuple(ONLINE=_online, OFFLINE=_offline, UNKNOWN=_unknown)

WIFI = _wifi_tuple(STATUS=_wifi_status, NETWORK=_wifi_network, INTERFACE=_wifi_interface,FREQUENCY=_wifi_frequency, SSID=_wifi_ssid)

# Access Point Services

_access_point_key = ["DHCPCD", "DNSMASQ", "HOSTAPD", "STATUS"]
_access_point_tuple = collections.namedtuple("service", _service_key)

_dhcpcd = "dhcpcd"
_dnsmasq = "dnsmasq"
_hostapd = "hostapd"


# Access Point Services Status Codes

_access_point_status_key = ["ACTIVE", "INACTIVE", "FAILED"]
_access_point_status_tuple = collections.namedtuple(
    "access_point", _access_point_status_key)

_active = 0x01
_inactive = 0x02
_failed = 0x03

_service_status = _service_status_tuple(
    ACTIVE=_active, INACTIVE=_inactive, FAILED=_failed)

ACCESSPOINT = _access_point_tuple(DHCPCD=_dhcpcd, DNSMASQ=_dnsmasq,
                         HOSTAPD=_hostapd, STATUS=_service_status)

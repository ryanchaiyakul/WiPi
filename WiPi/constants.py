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

# Network/Interface Status Codes
_status_key = ["ONLINE", "OFFLINE", "UNKNOWN"]

_status_tuple = collections.namedtuple("status", _status_key)

_online = 0x01
_offline = 0x02
_unknown = 0x03

STATUS = _status_tuple(ONLINE=_online, OFFLINE=_offline, UNKNOWN=_unknown)

# Access Point Services

_service_key = ["DHCPCD", "DNSMASQ", "HOSTAPD", "STATUS"]
_service_tuple = collections.namedtuple("service", _service_key)

_dhcpcd = "dhcpcd"
_dnsmasq = "dnsmasq"
_hostapd = "hostapd"


# Access Point Services Status Codes

_service_status_key = ["ACTIVE", "INACTIVE", "FAILED"]
_service_status_tuple = collections.namedtuple(
    "service_status", _service_status_key)

_active = 0x01
_inactive = 0x02
_failed = 0x03

_service_status = _service_status_tuple(
    ACTIVE=_active, INACTIVE=_inactive, FAILED=_failed)

SERVICE = _service_tuple(DHCPCD=_dhcpcd, DNSMASQ=_dnsmasq,
                         HOSTAPD=_hostapd, STATUS=_service_status)

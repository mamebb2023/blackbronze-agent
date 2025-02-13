import psutil
import socket
import requests


def network_info():
    """Returns MAC addresses and MTU values for all network interfaces."""
    info = {"network_interfaces": []}

    for interface, addrs in psutil.net_if_addrs().items():
        mac_address = None
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # Get MAC Address
                mac_address = addr.address

        mtu = psutil.net_if_stats().get(interface, None)
        mtu_value = mtu.mtu if mtu else "None"

        info["network_interfaces"].append(
            {"interface": interface, "mac_address": mac_address, "mtu": mtu_value}
        )

    return info


def network_metrics():
    """Returns network I/O statistics since boot."""
    io_stats = psutil.net_io_counters(pernic=True)
    interfaces = psutil.net_if_addrs()

    interface_info = [
        {
            "interface": iface,
            "ip_address": snic.address,
            "netmask": snic.netmask,
            "broadcast": snic.broadcast,
        }
        for iface, snics in interfaces.items()
        for snic in snics
        if snic.family == socket.AF_INET
    ]

    io_data = {
        nic: {
            "bytes_sent": s.bytes_sent,
            "bytes_recv": s.bytes_recv,
            "packets_sent": s.packets_sent,
            "packets_recv": s.packets_recv,
            "errin": s.errin,
            "errout": s.errout,
            "dropin": s.dropin,
            "dropout": s.dropout,
        }
        for nic, s in io_stats.items()
    }

    try:
        public_ip = requests.get("https://api.ipify.org").text
    except requests.RequestException:
        public_ip = "unknown"

    return {
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "public_ip": public_ip,
        "network_interfaces": interface_info,
        "network_io": io_data,
    }

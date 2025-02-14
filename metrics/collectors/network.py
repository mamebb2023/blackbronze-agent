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
    """Returns active network interfaces with their stats."""
    io_stats = psutil.net_io_counters(pernic=True)
    interfaces = psutil.net_if_addrs()

    active_interfaces = []

    for nic, s in io_stats.items():
        total_bytes = s.bytes_sent + s.bytes_recv
        if total_bytes > 0:  # Only consider interfaces with activity
            interface_info = {"interface": nic}

            # Try to find the IP details for this interface

            for iface, snics in interfaces.items():
                if iface == nic:
                    # for snic in snics:
                    # if snic.family in [socket.AF_INET, socket.AF_INET6]:  # Include both IPv4 and IPv6
                    #     interface_info.update({
                    #         "ip_address": snic.address,
                    #         "netmask": snic.netmask,
                    #         "broadcast": snic.broadcast if hasattr(snic, "broadcast") else None
                    #     })
                    #     break
                    for snic in snics:
                        if snic.family == socket.AF_INET:  # IPv4 only
                            interface_info.update(
                                {
                                    "ip_address": snic.address,
                                    "netmask": snic.netmask,
                                    "broadcast": snic.broadcast,
                                }
                            )
                            break

            # Add network usage stats
            interface_info.update(
                {
                    "total_bytes": total_bytes,
                    "bytes_sent": s.bytes_sent,
                    "bytes_recv": s.bytes_recv,
                    "packets_sent": s.packets_sent,
                    "packets_recv": s.packets_recv,
                    "errin": s.errin,
                    "errout": s.errout,
                    "dropin": s.dropin,
                    "dropout": s.dropout,
                }
            )

            active_interfaces.append(interface_info)

    # Get public IP (handle request failure)
    try:
        public_ip = requests.get("https://api.ipify.org", timeout=5).text
    except requests.RequestException:
        public_ip = "unknown"

    return {"public_ip": public_ip, "active_interfaces": active_interfaces}

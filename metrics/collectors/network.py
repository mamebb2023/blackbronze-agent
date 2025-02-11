import psutil
import socket


def network_info():
    """Returns network interface information."""
    info = {
        "network_interfaces": [],
    }

    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET:  # Use socket.AF_INET for IPv4
                info["network_interfaces"].append(
                    {
                        "interface": interface,
                        "ip_address": snic.address,
                        "netmask": snic.netmask,
                        "broadcast": snic.broadcast,
                    }
                )

    return info


def network_metrics():
    """Returns network I/O statistics since boot."""
    io_stats = psutil.net_io_counters(pernic=True)
    io_data = {}

    for nic, stats in io_stats.items():
        io_data[nic] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errin": stats.errin,
            "errout": stats.errout,
            "dropin": stats.dropin,
            "dropout": stats.dropout,
        }

    return {"network_io": io_data}


if __name__ == "__main__":
    print("Network Interface Info:", network_info())
    print("Network I/O Metrics:", network_metrics())

import platform
import socket

from collectors import cpu, memory, disk, network


def get_system_info():
    """Collect system information."""

    info = {
        "node_name": platform.node(),
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "cpu": cpu.cpu_info(),
        "memory": memory.memory_info(),
        "disk": disk.disk_info(),
        "network": network.network_info(),
    }

    return info

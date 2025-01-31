import platform
import socket
import requests


def get_system_info():
    """Collect system information."""
    try:
        public_ip = requests.get("https://api.ipify.org").text
    except requests.RequestException:
        public_ip = "Unable to get public IP"

    info = {
        "node_name": platform.node(),
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "public_ip": public_ip,
    }
    return info

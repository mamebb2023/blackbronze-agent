# Network metrics collection
import psutil

def network_usage():
  net_io = psutil.net_io_counters()
  return {
    "download": net_io.bytes_recv / (1024 * 1024),
    "upload": net_io.bytes_sent / (1024 * 1024)
  }


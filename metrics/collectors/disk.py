# Disk usage collector
import psutil

def disk_usage():
  return psutil.disk_usage("/").percent
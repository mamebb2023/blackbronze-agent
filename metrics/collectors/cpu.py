# CPU metrics collection 
import psutil

def cpu_usage():
    return psutil.cpu_percent(interval=1)
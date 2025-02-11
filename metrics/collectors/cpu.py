import psutil
import platform


def cpu_info():
    """Returns static CPU info."""
    info = {
        "cpu_name": platform.processor(),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_architecture": platform.architecture(),
    }

    if psutil.cpu_freq():
        info["cpu_freq"] = {
            "max": psutil.cpu_freq().max,
            "min": psutil.cpu_freq().min,
        }

    return info


def cpu_temperature():
    """Returns CPU temperature if supported by the system."""
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:  # For Intel CPUs
            cpu_temp = temps["coretemp"][0].current
        elif "k10temp" in temps:  # For AMD CPUs
            cpu_temp = temps["k10temp"][0].current
        else:
            cpu_temp = None

        return {"cpu_temperature": cpu_temp}  # in celsius
    except Exception as e:
        return {"cpu_temperature": None, "error": str(e)}


def cpu_metrics():
    """Returns dynamic CPU usage metrics."""
    usage = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_freq": (psutil.cpu_freq().current if psutil.cpu_freq() else None),
        "cpu_times": {
            "user": psutil.cpu_times().user,
            "system": psutil.cpu_times().system,
            "idle": psutil.cpu_times().idle,
        },
        "cpu_times_percent": psutil.cpu_times_percent(interval=1),
    }
    cpu_temp = cpu_temperature()

    if not cpu_temp["error"]:
        usage["cpu_temperature"] = cpu_temp["cpu_temperature"]

    if psutil.LINUX:
        usage["cpu_times"].update(
            {
                "nice": psutil.cpu_times().nice,
                "iowait": psutil.cpu_times().iowait,
                "irq": psutil.cpu_times().irq,
                "softirq": psutil.cpu_times().softirq,
                "steal": psutil.cpu_times().steal,
                "guest": psutil.cpu_times().guest,
                "guest_nice": psutil.cpu_times().guest_nice,
            }
        )

    return usage

import psutil
import platform


def cpu_info():
    """Returns static CPU info."""
    info = {
        "cpu_name": platform.processor(),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_architecture": " ".join(platform.architecture()),
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
    """Returns optimized and detailed CPU usage metrics."""

    # Get overall CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_times = psutil.cpu_times_percent(interval=1)

    # Prepare CPU usage details
    metrics = {
        "cpu_percent": cpu_percent,  # Overall CPU usage
        "cpu_times_percent": {
            "user": cpu_times.user,
            "system": cpu_times.system,
            "idle": cpu_times.idle,
        },
    }

    # Add extra details if running on Linux
    # if psutil.LINUX:
    #     metrics["cpu_times_percent"].update(
    #         {
    #             "nice": cpu_times.nice,
    #             "iowait": cpu_times.iowait,
    #             "irq": cpu_times.irq,
    #             "softirq": cpu_times.softirq,
    #             "steal": cpu_times.steal,
    #             "guest": cpu_times.guest,
    #             "guest_nice": cpu_times.guest_nice,
    #         }
    #     )

    # Try to get CPU temperature (if supported)
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            metrics["cpu_temperature"] = temps["coretemp"][
                0
            ].current  # Get the first sensor value
    except AttributeError:
        metrics["cpu_temperature"] = "Unavailable"

    return metrics

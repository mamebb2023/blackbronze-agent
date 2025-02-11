import psutil


def disk_info():
    """Returns disk usage statistics for all mounted partitions."""
    info = {
        "disk_total_space": psutil.disk_usage("/").total,
        "disk_partitions": [],
    }

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            # Append partition information to the "partitions" list
            info["disk_partitions"].append(
                {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "space": usage.total,
                    "fstype": partition.fstype,
                }
            )
        except PermissionError:
            # Skip partitions that can't be accessed
            continue

    return info


def disk_metrics():
    metrics = {
        "disk_space_used": psutil.disk_usage("/").used,
        "disk_space_free": psutil.disk_usage("/").free,
        "disk_space_percent": psutil.disk_usage("/").percent,
        "disk_io": disk_io(),
    }

    return metrics


def disk_io():
    """Returns disk I/O statistics since boot."""
    io_stats = psutil.disk_io_counters(perdisk=True)
    io_data = {}
    for disk, stats in io_stats.items():
        io_data[disk] = {
            "read_count": stats.read_count,
            "write_count": stats.write_count,
            "read_bytes": stats.read_bytes,
            "write_bytes": stats.write_bytes,
            "read_time": stats.read_time,
            "write_time": stats.write_time,
        }

    return io_data

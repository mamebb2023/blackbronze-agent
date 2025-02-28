import psutil


def running_services():
    services = []

    # Get all processes with their PID and name
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        pid = proc.info["pid"]
        service_name = proc.info["name"]

        # Get network connections for this process
        connections = [
            conn for conn in psutil.net_connections(kind="inet") if conn.pid == pid
        ]

        # If process has network connections, list them
        if connections:
            for conn in connections:
                services.append(
                    {
                        "pid": pid,
                        "service": service_name,
                        "local_address": (
                            f"{conn.laddr.ip}:{conn.laddr.port}"
                            if conn.laddr
                            else "None"
                        ),
                        "status": conn.status,
                    }
                )
        else:
            # Process exists but has no network connections
            services.append(
                {
                    "pid": pid,
                    "service": service_name,
                    "local_address": "None",
                    "status": "N/A",
                }
            )

    return services

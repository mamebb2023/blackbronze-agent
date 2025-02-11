import psutil

# import wmi


def memory_info():
    """Returns static memory info (e.g., total, available, etc.)."""
    virtual_mem = psutil.virtual_memory()

    # c = wmi.WMI()
    # for memory in c.Win32_PhysicalMemory():
    #     print(f"Memory Manufacturer: {memory.Manufacturer}")
    #     print(f"Memory Type: {memory.MemoryType}")

    # # Safely handle buffers and cached
    info = {
        "total": virtual_mem.total,  # Static: Total physical memory
        # "slots": [],  # Static: Memory type
    }

    # Static: Memory shared between processes
    if hasattr(virtual_mem, "shared"):
        info["shared"] = virtual_mem.shared

    # Static: Cache used for block device I/O
    if hasattr(virtual_mem, "buffers"):
        info["buffers"] = virtual_mem.buffers

    # Static: Memory used by the page cache
    if hasattr(virtual_mem, "cached"):
        info["cached"] = virtual_mem.cached

    return info


def memory_metrics():
    """Returns dynamic memory usage metrics."""
    virtual_mem = psutil.virtual_memory()
    metrics = {
        "available": virtual_mem.available,  # Dynamic: Memory available for new processes
        "used": virtual_mem.used,  # Dynamic: Memory currently being used
        "free": virtual_mem.free,  # Static: Total free memory
        "percent": virtual_mem.percent,  # Dynamic: Memory usage percentage
    }

    # Dynamic: Memory used recently
    if hasattr(virtual_mem, "active"):
        memory_metrics["active"] = virtual_mem.active

    # Dynamic: Memory not recently used
    if hasattr(virtual_mem, "inactive"):
        memory_metrics["inactive"] = virtual_mem.inactive

    return metrics


# def swap_memory_usage():
#     """Returns static and dynamic swap memory metrics."""
#     swap_mem = psutil.swap_memory()
#     return {
#         "total": swap_mem.total,  # Static: Total swap memory
#     }, {
#         "free": swap_mem.free,  # Static: Free swap memory
#         "used": swap_mem.used,  # Dynamic: Swap memory used
#         "percent": swap_mem.percent,  # Dynamic: Swap usage percentage
#         "sin": swap_mem.sin,  # Dynamic: Bytes swapped in from disk
#         "sout": swap_mem.sout,  # Dynamic: Bytes swapped out to disk
#     }


if __name__ == "__main__":
    print("Virtual Memory Info (Static):", memory_info())
    print("Virtual Memory Metrics (Dynamic):", memory_metrics())

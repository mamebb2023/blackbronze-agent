import psutil
import wmi


def memory_info():
    """Returns static memory info (e.g., total, available, etc.)."""
    virtual_mem = psutil.virtual_memory()

    info = {
        "total": virtual_mem.total,
    }

    if hasattr(virtual_mem, "shared"):
        info["shared"] = virtual_mem.shared

    if hasattr(virtual_mem, "buffers"):
        info["buffers"] = virtual_mem.buffers

    if hasattr(virtual_mem, "cached"):
        info["cached"] = virtual_mem.cached

    try:
        c = wmi.WMI()
        physical_memory_arrays = c.Win32_PhysicalMemoryArray()

        if physical_memory_arrays:
            slots = 0
            physical_memories = c.Win32_PhysicalMemory()
            for memory in physical_memories:
                if memory.BankLabel:
                    slots += 1
            info["slots"] = slots  # Add the slot count to the info dictionary
        else:
            info["slots"] = "unknown"  # No physical memory arrays found

    except Exception as e:
        print(f"Error getting RAM slots: {e}")
        info["slots"] = "unknown"

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

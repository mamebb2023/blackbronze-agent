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
            info["slots"] = None  # No physical memory arrays found

    except Exception as e:
        print(f"Error getting RAM slots: {e}")
        info["slots"] = None  # Indicate that slot information couldn't be retrieved.

    return info

# Metrics manager
import aiohttp
from datetime import datetime

from utils.logger import log_error
from config.config import BACKEND_URL
from collectors import cpu, disk, memory, network


def get_system_metrics():
    """Collect system metrics."""

    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu": cpu.cpu_metrics(),
        "memory": memory.memory_metrics(),
        "disk": disk.disk_metrics(),
        "network": network.network_metrics(),
    }

    return metrics


async def send_data(metrics, api_key, agent_id, status):
    """Send metrics data to website back-end."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    metrics["agent_id"] = agent_id
    metrics["status"] = status

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/api/agent/metrics", json=metrics, headers=headers
            ) as response:
                print("Backend Response:", response.status, await response.text())
                response.raise_for_status()
                print("Data sent successfully:", await response.json())
    except aiohttp.ClientError as e:
        log_error(f"Failed to send data: {e}")
        raise

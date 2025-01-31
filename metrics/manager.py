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
        "cpu_usage": cpu.cpu_usage(),
        "memory_usage": memory.memory_usage(),
        "disk_usage": disk.disk_usage(),
        "network_usage": network.network_usage(),
    }

    return metrics


async def send_data(metrics, api_key, agent_id):
    """Send metrics data to website back-end."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    metrics["agent_id"] = agent_id

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

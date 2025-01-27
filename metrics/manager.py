# Metrics manager
import requests
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


def send_data(metrics, api_key, agent_id):
    """Send the collected metrics to the backend."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Attach the agent ID to the metrics
    metrics["agent_id"] = agent_id

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/agent/metrics", json=metrics, headers=headers
        )
        response.raise_for_status()
        print("Data sent successfully:", response.json())
    except requests.exceptions.RequestException as e:
        log_error(f"Failed to send data: {e}")

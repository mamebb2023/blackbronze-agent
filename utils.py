import psutil
import logging
import os
import uuid
import json
import requests

from config import ERROR_LOG_FILE, AGENT_CONFIG_FILE, BACKEND_URL
from datetime import datetime

def register_agent(api_key):
    """Register the agent with the backend."""
    agent_id = get_or_create_agent_id()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"agent_id": agent_id, "api_key": api_key}

    print("Registering Agent with Payload:", payload)

    try:
        response = requests.post(f"{BACKEND_URL}/api/agent/register", json=payload, headers=headers)
        print("Backend Response:", response.status_code, response.text)
        response.raise_for_status()
        print("Agent registered successfully:", response.json())
    except requests.exceptions.RequestException as e:
        log_error(f"Failed to register agent: {e}")
        raise


def get_or_create_agent_id():
  """Get or create an agent ID."""
  
  if os.path.exists(AGENT_CONFIG_FILE):
    with open(AGENT_CONFIG_FILE, "r") as f:
      config = json.load(f)
      return config.get("agent_id")

  agent_id = str(uuid.uuid4())
  with open(AGENT_CONFIG_FILE, "w") as f:
    json.dump({"agent_id": agent_id}, f)

  return agent_id


def get_system_metrics():
  """Collect system metrics."""
  net_io = psutil.net_io_counters()
  metrics = {
    "cpu_usage": psutil.cpu_percent(interval=1),
    "memory_usage": psutil.virtual_memory().percent,
    "disk_usage": psutil.disk_usage("/").percent,
    "network_usage": {
      "download": net_io.bytes_recv / (1024 * 1024),
      "upload": net_io.bytes_sent / (1024 * 1024)
    },
    "timestamp": datetime.now().isoformat()
  }

  return metrics


def send_data(metrics, api_key, agent_id):
  """Send the collected metrics to the backend."""
  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }

  # Attach the agent ID to the metrics
  metrics["agent_id"] = agent_id

  try:
    response = requests.post(f"{BACKEND_URL}/api/agent/metrics", json=metrics, headers=headers)
    response.raise_for_status()
    print("Data sent successfully:", response.json())
  except requests.exceptions.RequestException as e:
    log_error(f"Failed to send data: {e}")


def log_error(message):
  """Log error messages."""
  logging.basicConfig(filename=ERROR_LOG_FILE, level=logging.ERROR)
  logging.error(f"{datetime.now} - {message}")

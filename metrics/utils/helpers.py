# Helper functions

import os
import uuid
import json
import requests

from utils.logger import log_error
from config.config import BACKEND_URL, AGENT_CONFIG_FILE


def register_agent(api_key):
    """Register the agent with the backend."""
    agent_id = get_or_create_agent_id()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"agent_id": agent_id, "api_key": api_key}

    print("Registering Agent with Payload:", payload)

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/agent/register", json=payload, headers=headers
        )
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

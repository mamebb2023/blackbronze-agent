import aiofiles
import aiohttp
import os
import json
import uuid

from collectors.info import get_system_info
from utils.logger import log_error
from config.config import BACKEND_URL, AGENT_CONFIG_FILE


async def get_or_create_agent_id():
    """Get or create an agent ID."""
    config_dir = os.path.dirname(AGENT_CONFIG_FILE)

    # Ensure the directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Check if the file exists and read it
    if os.path.exists(AGENT_CONFIG_FILE):
        async with aiofiles.open(AGENT_CONFIG_FILE, "r") as f:
            config = json.loads(await f.read())
            return config.get("agent_id")

    # If the file doesn't exist, generate a new agent_id
    agent_id = str(uuid.uuid4())
    async with aiofiles.open(AGENT_CONFIG_FILE, "w") as f:
        await f.write(json.dumps({"agent_id": agent_id}))

    return agent_id


async def register_agent(api_key):
    """Register the agent with the backend."""

    agent_id = await get_or_create_agent_id()
    device_info = get_system_info()

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"agent_id": agent_id, "api_key": api_key, "device_info": device_info}

    print("Registering Agent with Payload:")
    for key, value in payload.items():
        print(f"{key}: {value}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/api/agent/register", json=payload, headers=headers
            ) as response:
                print("Backend Response:", response.status, await response.text())
                response.raise_for_status()
                print("Agent registered successfully:", await response.json())
    except aiohttp.ClientError as e:
        log_error(f"Failed to register agent: {e}")
        raise

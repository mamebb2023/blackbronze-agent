# Main agent script that runs on the client machine to collect system metrics and send them to the server.

import time
import asyncio

from collectors.info import get_system_info
from utils.helpers import get_or_create_agent_id, register_agent
from cli import parse_arguments
from manager import get_system_metrics, send_data


async def main(api_key):
    """Main agent function."""
    print("BlackBronze Agent is running...")

    # Register the agent when start before running
    await register_agent(api_key)

    while True:
        metrics = get_system_metrics()
        agent_id = await get_or_create_agent_id()
        await send_data(metrics, api_key, agent_id)
        time.sleep(60)


if __name__ == "__main__":
    api_key = parse_arguments()
    asyncio.run(main(api_key))

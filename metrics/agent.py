# import time
import asyncio

from utils.helpers import get_or_create_agent_id, register_agent
from cli import parse_arguments
from manager import get_system_metrics, send_data


async def main(api_key):
    """Main agent function."""

    # Register the agent when start before running
    await register_agent(api_key)

    print("\033[92mBlackBronze Agent is running...\033[0m")
    while True:
        try:
            metrics = get_system_metrics()
            agent_id = await get_or_create_agent_id()
            await send_data(metrics, api_key, agent_id, "online")
            await asyncio.sleep(15)
        except Exception as e:
            metrics = get_system_metrics()
            agent_id = get_or_create_agent_id()
            asyncio.run(send_data(metrics, api_key, agent_id, "offline"))
            print(f"\033[91mError occurred: {e}\033[0m")


if __name__ == "__main__":
    api_key = parse_arguments()

    try:
        asyncio.run(main(api_key))
    except KeyboardInterrupt:
        metrics = get_system_metrics()
        agent_id = asyncio.run(get_or_create_agent_id())
        asyncio.run(send_data(metrics, api_key, agent_id, "offline"))

        print("\033[91mKeyBoardInterrupt: BlackBronze Agent is stopped.\033[0m")
        exit(1)

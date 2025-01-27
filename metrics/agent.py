# Main agent script that runs on the client machine to collect system metrics and send them to the server.

import time

from utils.helpers import get_or_create_agent_id, register_agent
from cli import parse_arguments
from manager import get_system_metrics, send_data


def main(api_key):
    """Main agent function."""
    print("BlackBronze Agent is running...")

    # Register the agent when start before running
    register_agent(api_key)

    while True:
        metrics = get_system_metrics()
        agent_id = get_or_create_agent_id()
        send_data(metrics, api_key, agent_id)
        time.sleep(60)


if __name__ == "__main__":
    api_key = parse_arguments()
    main(api_key)

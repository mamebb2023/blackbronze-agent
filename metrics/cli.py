# Command-line interface
import argparse


def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="Start the BlackBronze agent.")
    parser.add_argument(
        "--BB_API_KEY",
        type=str,
        required=True,
        help="API key for the authenticating the agent to the backend",
    )

    args = parser.parse_args()

    api_key = args.BB_API_KEY
    if not api_key:
        raise ValueError("API key (--BB_API_KEY) is required to run the agent.")

    return api_key

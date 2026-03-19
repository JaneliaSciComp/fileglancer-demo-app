"""Fileglancer Demo App - a simple script for testing job submission."""

import argparse
import os
import time
import sys
from datetime import datetime
from loguru import logger


def main():
    parser = argparse.ArgumentParser(description="Fileglancer Demo App")
    parser.add_argument(
        "--sleep_seconds", type=int, default=5,
        help="Number of seconds to sleep between messages",
    )
    parser.add_argument(
        "--message", type=str, default="Hello from Fileglancer!",
        help="Message to print",
    )
    parser.add_argument(
        "--repeat", type=int, default=1,
        help="Number of times to repeat the message",
    )
    parser.add_argument(
        "--output_dir", type=str, default="",
        help="Directory to write output file (optional)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--log_level", type=str, default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    args = parser.parse_args()

    # Configure logging based on the log level in the settings
    logger.remove()
    logger.add(sys.stderr, level=args.log_level)

    print("=== Fileglancer Demo App ===")
    logger.info(f"Sleep seconds: {args.sleep_seconds}")
    logger.info(f"Message: {args.message}")
    logger.info(f"Repeat: {args.repeat}")
    logger.info(f"Output dir: {args.output_dir or '<none>'}")
    logger.info(f"Verbose: {args.verbose}")
    logger.info(f"Log level: {args.log_level}")

    for i in range(1, args.repeat + 1):
        print(f"[{i}/{args.repeat}] {args.message}")
        if args.verbose:
            print(f"  Sleeping for {args.sleep_seconds} seconds...")
        time.sleep(args.sleep_seconds)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, "demo-output.txt")
        logger.info(f"Writing output to {output_file}")
        with open(output_file, "w") as f:
            f.write(f"Demo completed at {datetime.now()}\n")
            f.write(f"Message: {args.message}\n")
            f.write(
                f"Repeated {args.repeat} times with "
                f"{args.sleep_seconds} second intervals\n"
            )

    print("Done!")


if __name__ == "__main__":
    main()

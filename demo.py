"""Fileglancer Demo App - a simple script for testing job submission."""

import argparse
import os
import time
from datetime import datetime


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
    args = parser.parse_args()

    print("=== Fileglancer Demo App ===")
    print(f"Sleep seconds: {args.sleep_seconds}")
    print(f"Message: {args.message}")
    print(f"Repeat: {args.repeat}")
    print(f"Output dir: {args.output_dir or '<none>'}")
    print(f"Verbose: {args.verbose}")
    print("============================")
    print()

    for i in range(1, args.repeat + 1):
        print(f"[{i}/{args.repeat}] {args.message}")
        if args.verbose:
            print(f"  Sleeping for {args.sleep_seconds} seconds...")
        time.sleep(args.sleep_seconds)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, "demo-output.txt")
        print(f"Writing output to {output_file}")
        with open(output_file, "w") as f:
            f.write(f"Demo completed at {datetime.now()}\n")
            f.write(f"Message: {args.message}\n")
            f.write(
                f"Repeated {args.repeat} times with "
                f"{args.sleep_seconds} second intervals\n"
            )

    print()
    print("Done!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import pprint
import subscriptions

def parse_args():
    """
    Parses the command line arguments and calls the appropriate function for the selected subcommand.
    """
    parser = argparse.ArgumentParser("Terrain API Client")
    parser.add_argument(
        "-e", "--env",
        help="the DE environment to work with",
        choices=["prod", "qa"],
        default="prod"
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands"
    )
    subscriptions.add_subparser(subparsers)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    args.func(args)

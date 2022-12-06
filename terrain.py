#!/usr/bin/env python3

import argparse
import pprint
import subscriptions

def add_subparser_for_module(subparsers, module):
    """
    Adds an argument subparser for a module.
    """
    subcommand, *aliases = module.list_module_subcommands()
    description = module.get_module_description()
    parser = subparsers.add_parser(subcommand, aliases=aliases, description=description)
    module.config_argument_parser(parser)

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
    add_subparser_for_module(subparsers, subscriptions)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    args.func(args)

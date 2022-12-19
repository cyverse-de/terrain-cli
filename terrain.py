#!/usr/bin/env python3

import argparse
import os
import pprint
import subcommands
import subscriptions
import sys

GREEN="\033[92m"
NORMAL="\033[0m"

def add_subparser_for_module(subparsers, module):
    """
    Adds an argument subparser for a module.
    """
    subcommand, *aliases = module.list_module_subcommands()
    description = module.get_module_description()
    subcommands.add_subcommand_description(subcommand, aliases, description)
    parser = subparsers.add_parser(subcommand, aliases=aliases, description=description)
    module.config_argument_parser(parser)

def parse_args():
    """
    Parses the command line arguments and calls the appropriate function for the selected subcommand.
    """
    parser = argparse.ArgumentParser(
        "Terrain API Client",
        description="Use {0}{1} help{2} to list available subcommands.".format(GREEN, sys.argv[0], NORMAL)
    )
    parser.add_argument(
        "-e", "--env",
        help="the DE environment to work with",
        choices=["prod", "qa"],
        default="prod"
    )
    subparsers = parser.add_subparsers(metavar="subcommand", dest="command")

    # Add subparsers and keep a record of the available subcommands.
    add_subparser_for_module(subparsers, subscriptions)
    subcommands.add_subcommand_subparser(subparsers)

    return parser.parse_args()

if __name__ == "__main__":
    # Enable ANSI escape codes in the terminal.
    os.system("")

    # Parse the command-line arguments.
    args = parse_args()

    # Call the subcommand function.
    args.func(args)

#!/usr/local/env python3

# A listing of subcommands used to display the information later.
subcommands = {"help": "list available subcommands"}

def add_subcommand_description(subcommand, aliases, description):
    """
    Adds a subcommand description to the subcommand listing.
    """
    subcommands[subcommand] = "{0} ({1})".format(description, ",".join(aliases))

def list_subcommands(args):
    """
    Lists subcommands available to the user.
    """
    print("\nThe following subcommands are available:\n")
    for subcommand in sorted(subcommands.keys()):
        print("    {0}: {1}".format(subcommand, subcommands[subcommand]))

def add_subcommand_subparser(subparsers):
    """
    Adds a subparser for listing available subcommands.
    """
    parser = subparsers.add_parser("help", description="list available subcommands")
    parser.set_defaults(func=list_subcommands)

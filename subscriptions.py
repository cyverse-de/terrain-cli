#!/usr/bin/env python3

import argparse
import client
import jwt
import pprint
import sys

def list_plans(args):
    """
    Lists available subscription plans.
    """
    plans = client.list_plans(args.env)
    for plan in plans:
        print("{0}:".format(plan["name"]))
        for quota_default in sorted(plan["plan_quota_defaults"], key=lambda qd: qd["resource_type"]["name"]):
            print("    {0}: {1}".format(quota_default["resource_type"]["name"], quota_default["quota_value"]))

def display_subscription(subscription):
    """
    Displays the given subscription.
    """
    print("Effective Starting:", subscription["effective_start_date"])
    print("Expires At:", subscription["effective_end_date"])
    print("Plan:", subscription["plan"]["name"])
    print("Quotas:")
    quotas = subscription["quotas"] if "quotas" in subscription else []
    for quota in sorted(quotas, key=lambda q: q["resource_type"]["name"]):
        print("    {0}: {1}".format(quota["resource_type"]["name"], quota["quota"]))
    print("Usages:")
    usages = subscription["usages"] if "usages" in subscription else []
    for usage in sorted(usages, key=lambda u: u["resource_type"]["name"]):
        print("    {0}: {1}".format(usage["resource_type"]["name"], usage["usage"]))

def get_subscription(args):
    """
    Gets the subscription for a user. If the username is unspecified or is the same as the authenticated user's username
    then the user's current subscription is obtained using the non-admin endpoint. Otherwise, the admin end point is
    called to get the current user's subscription.
    """
    user = args.user
    if user is not None:
        auth_user = jwt.get_username(client.get_access_token(args.env))
        if auth_user != user:
            display_subscription(client.admin_get_subscription(args.env, user))
            return
    display_subscription(client.get_subscription(args.env))

def list_module_subcommands():
    """
    Returns a list of subcommands that are used to access thismodule.
    """
    return ["subscriptions", "subscription", "sub", "subs"]

def get_module_description():
    """
    Returns a brief description of the module.
    """
    return "subscription operations"

def display_module_help(args):
    """
    Displays the help for the module.
    """
    prog = sys.argv[0]

    print("Terrain Subscriptions Operations")
    print()
    print("This command provides additional subcommands to get and update subscription")
    print("information for users. The available subcommands are:")
    print()
    print(prog, args.command, "list-plans")
    print(prog, args.command, "plans")
    print(prog, args.command, "lp")
    print()
    print("Summarizes each of the available CyVerse subscription plans.")
    print()
    print(prog, args.command, "get")
    print(prog, args.command, "get -u username")
    print()
    print("Gets information about the current subscription. If the username is not provided")
    print("or happens to be the username of the currently authenticated user then admin")
    print("access is not required and the user's current subscription is displayed.")
    print()
    print("If the username is provided and is not the username of the currently authenticated")
    print("user then admin access is required. If the authenticated user has admin access then")
    print("information about the currently active subscription of the specified user will be")
    print("displayed.")
    print()
    print(prog, args.command, "help")
    print()
    print("Display this help message.")

def config_argument_parser(parser):
    """
    Configures the argument parser for the module.
    """
    subparsers = parser.add_subparsers()

    # Lists plans.
    parser_list_plans = subparsers.add_parser("list-plans", aliases=["plans", "lp"])
    parser_list_plans.set_defaults(func=list_plans)

    # Displays the current subscription for a user.
    parser_get_subscription = subparsers.add_parser("get")
    parser_get_subscription.add_argument("-u", "--user", help="the username of the user to get the subscription for")
    parser_get_subscription.set_defaults(func=get_subscription)

    # Displays the help for this module.
    parser_show_help = subparsers.add_parser("help")
    parser_show_help.set_defaults(func=display_module_help)

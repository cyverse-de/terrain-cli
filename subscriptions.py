#!/usr/bin/env python3

import argparse
import client
import jwt
import pprint

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

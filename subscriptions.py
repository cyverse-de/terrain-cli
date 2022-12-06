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
            print("\t{0}: {1}".format(quota_default["resource_type"]["name"], quota_default["quota_value"]))

def display_subscription(subscription):
    """
    Displays the given subscription.
    """
    print("Effective Starting:", subscription["effective_start_date"])
    print("Expires At:", subscription["effective_end_date"])
    print("Plan:", subscription["plan"]["name"])
    print("Quotas:")
    for quota in sorted(subscription["quotas"], key=lambda q: q["resource_type"]["name"]):
        print("\t{0}: {1}".format(quota["resource_type"]["name"], quota["quota"]))
    print("Usages:")
    for usage in sorted(subscription["usages"], key=lambda u: u["resource_type"]["name"]):
        print("\t{0}: {1}".format(usage["resource_type"]["name"], usage["usage"]))

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

def add_subparser(main_subparsers):
    """
    Adds the subparser for the subscriptions subcommand.
    """
    parser = main_subparsers.add_parser(
        "subscriptions",
        aliases=["subscription", "sub", "subs"],
        description="subscription operations"
    )
    subparsers = parser.add_subparsers()

    # Lists plans.
    parser_list_plans = subparsers.add_parser("list-plans", aliases=["plans", "lp"])
    parser_list_plans.set_defaults(func=list_plans)

    # Displays the current subscription for a user.
    parser_get_subscription = subparsers.add_parser("get")
    parser_get_subscription.add_argument("-u", "--user", help="the username of the user to get the subscription for")
    parser_get_subscription.set_defaults(func=get_subscription)

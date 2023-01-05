#!/usr/bin/env python3

import argparse
import client
import jwt
import pprint
import re
import sys

# Unit conversions
conversions = {
    "": 1,
    "K": 2**10,
    "k": 2**10,
    "M": 2**20,
    "m": 2**20,
    "G": 2**30,
    "g": 2**30,
    "T": 2**40,
    "t": 2**40,
}

def list_plans(args):
    """
    Lists available subscription plans.
    """
    plans = client.list_plans(args.env)
    for plan in plans:
        print("{0}:".format(plan["name"]))
        for quota_default in sorted(plan["plan_quota_defaults"], key=lambda qd: qd["resource_type"]["name"]):
            print("    {0}: {1}".format(quota_default["resource_type"]["name"], quota_default["quota_value"]))

def list_resource_types(args):
    """
    Lists available resource types.
    """
    resource_types = client.list_resource_types(args.env)
    for resource_type in resource_types:
        print("{0}: {1}".format(resource_type["name"], resource_type["unit"]))

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
            if not client.is_valid_username(args.env, user):
                print("user does not exist:", user, file=sys.stderr)
                return
            display_subscription(client.admin_get_subscription(args.env, user))
            return
    display_subscription(client.get_subscription(args.env))

def add_subscription(args):
    """
    Subscribes a user to a subscription plan. The subscription starts when the command is issued and ends after one
    year. Administrative access is required to use this subcommand.
    """
    user = args.user
    if not client.is_valid_username(args.env, user):
        print("user does not exist:", user, file=sys.stderr)
        sys.exit(1)
    plan = client.validate_plan_name(args.env, args.plan)
    if plan is None:
        print("plan does not exist:", args.plan, file=sys.stderr)
        sys.exit(1)
    client.admin_add_subscription(args.env, user, plan)
    display_subscription(client.admin_get_subscription(args.env, user))

def convert_quota(spec):
    """
    Converts a quota specification to a raw quota. The quota should be specified in numbers and unit conversions.
    Supported unit conversions are K (2^10 or 1024 units), M (2^20 units), G (2^30 units) and T (2^40 units). For
    example, a specification of 2K will be converted to 2*2^20 or 2048.
    """
    m = re.match(r'^(\d+(?:\.\d+)?)\s?([KkMmGgTt])?$', spec)
    if m is None:
        return None
    conversion = m.group(2) or ""
    if conversion not in conversions:
        return None
    return int(float(m.group(1)) * conversions[conversion])

def set_quota(args):
    """
    Sets the quota for a user's currently active subscription. If no active subscription exists, a new subscription for
    the default subscription plan will be created before the quota is updated.
    """
    user = args.user
    if not client.is_valid_username(args.env, user):
        print("user does not exist:", user, file=sys.stderr)
        sys.exit(1)
    resource_type = client.validate_resource_type_name(args.env, args.resource_type)
    if resource_type is None:
        print("resource type does not exist:", args.resource_type, file=sys.stderr)
        sys.exit(1)
    quota = convert_quota(args.quota)
    if quota is None:
        print("invalid quota specification:", args.quota, file=sys.stderr)
        sys.exit(1)
    display_subscription(client.admin_set_quota(args.env, user, resource_type, quota))

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
    print(prog, args.command, "list-resource-types")
    print(prog, args.command, "resource-types")
    print(prog, args.command, "lrt")
    print(prog, args.command, "rt")
    print()
    print("Summarizes each of the resource types supported by CyVerse.")
    print()
    print(prog, args.command, "get")
    print(prog, args.command, "get --user username")
    print(prog, args.command, "get -u username")
    print()
    print("options:")
    print("  --user username, -u username")
    print("                        the username of the user to get subscription informaton for")
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
    print(prog, args.command, "add --user username --plan plan")
    print(prog, args.command, "add -u username -p plan")
    print()
    print("options:")
    print("  --user usermame, -u username")
    print("                        the username of the user to create the subscription for")
    print("  --plan plan_name, -p plan_name")
    print("                        the name of the plan to subscribe the user to")
    print()
    print("Subscribes a user to a plan. The plan will be effective as of the time the command")
    print("is processed, and it will expire after one year. Admin accessis is required to use")
    print("this command.")
    print()
    print(prog, args.command, "set-quota --user username --resource-type resource-type --quota quota")
    print(prog, args.command, "set-quota -u username -r resource-type -q quota")
    print()
    print("options:")
    print("  --user username, -u username")
    print("                        the username of the user to update the quota for")
    print("  --resource-type resource-type, -r resource-type")
    print("                        the name of the resource type to update the quota for")
    print("  --quota quota, -q quota")
    print("                        the new resource usage limit")
    print()
    print("Updates a quota in the user's currently active subscription plan. If the user doesn't have")
    print("an active subscription, a new subscription of the default type will be created and the quota")
    print("will be updated in the new subscription. If the subscription plan doesn't have a quota for the")
    print("specified resource type then a new quota for the specified resource type will be added.")
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

    # Lists resource types.
    parser_list_resource_types = subparsers.add_parser("list-resource-types", aliases=["resource-types", "lrt", "rt"])
    parser_list_resource_types.set_defaults(func=list_resource_types)

    # Displays the current subscription for a user.
    parser_get_subscription = subparsers.add_parser("get")
    parser_get_subscription.add_argument("-u", "--user")
    parser_get_subscription.set_defaults(func=get_subscription)

    # Creates a new subscription for a user.
    parser_add_subscription = subparsers.add_parser("add")
    parser_add_subscription.add_argument("-u", "--user", required=True)
    parser_add_subscription.add_argument("-p", "--plan", required=True)
    parser_add_subscription.set_defaults(func=add_subscription)

    # Updates a quota for a user.
    parser_set_quota = subparsers.add_parser("set-quota")
    parser_set_quota.add_argument("-u", "--user", required=True)
    parser_set_quota.add_argument("-r", "--resource-type", required=True)
    parser_set_quota.add_argument("-q", "--quota",required=True)
    parser_set_quota.set_defaults(func=set_quota)

    # Displays the help for this module.
    parser_show_help = subparsers.add_parser("help")
    parser_show_help.set_defaults(func=display_module_help)

# Terrain CLI

Command-Line interface for the CyVerse Terrain API.

## Getting Help

Aliases: `help`

Lists available subcommands:

```
$ ./terrain.py help

The following subcommands are available:

    help: list available subcommands
    subscriptions: subscription operations (subscription,sub,subs)
```

## Subscriptions

Aliases: `subscriptions`, `subscription`, `sub`, `subs`

The subscriptions subcommand provides a command-line interface to API endpoints that can query and update subscription
information.

### List Plans

Aliases: `list-plans`, `plans`, `lp`

Lists information about available subscription plans:

```
$ ./terrain.py subs plans
Basic:
    cpu.hours: 20.0
    data.size: 5368709120.0
Regular:
    cpu.hours: 100.0
    data.size: 53687091200.0
Pro:
    cpu.hours: 2000.0
    data.size: 3298534883328.0
Commercial:
    cpu.hours: 5000.0
    data.size: 5497558138880.0
```

### Get Subscription

Aliases: `get`

Gets information about the currently active subscription for a single user. If the username argument is unspecified or
equal to the username of the authenticated user then the non-admin endpoint is used to obtain the authenticated user's
current subscription:

```
$ ./terrain.py sub get
Effective Starting: 2022-10-10T14:57:42.271394-07:00
Expires At: 2023-10-10T14:57:42.271394-07:00
Plan: Pro
Quotas:
    cpu.hours: 2000.0
    data.size: 3298534883328.0
Usages:
    cpu.hours: 303.87765671888894
    data.size: 12657134475.0
```

If the username argument is specified and not equal to the username of the authenticated user then the administrative
endpoint is called to get information about the current subscription for that user:

```
$ ./terrain.py sub get --user ipcdev
Effective Starting: 2022-11-20T09:15:39.727099-07:00
Expires At: 2023-11-20T09:15:39.727099-07:00
Plan: Commercial
Quotas:
    cpu.hours: 5000.0
    data.size: 5497558138880.0
Usages:
    data.size: 2992226992.0
```

### Add Subscription

Aliases: `add`

Subscribes a user to a subscription plan. The `--user` and `--plan` arguments are required for this command, and admin
access is always required. The specified user will be subscribed to the specified plan. The subscription will be
effective beginning when the command is processed, and it will expire after one year:

```
$ ./terrain.py subs add -u ipcdev -p Commercial
Effective Starting: 2022-12-06T17:03:57.237094-07:00
Expires At: 2023-12-06T17:03:57.237094-07:00
Plan: Commercial
Quotas:
    cpu.hours: 5000.0
    data.size: 5497558138880.0
Usages:
```

### Getting Subscription Help

Aliases: `help`

Displays information about all available subscriptions subcommands:

```
$ ./terrain.py subs help
Terrain Subscriptions Operations

This command provides additional subcommands to get and update subscription
information for users. The available subcommands are:

./terrain.py subs list-plans
./terrain.py subs plans
./terrain.py subs lp

Summarizes each of the available CyVerse subscription plans.

./terrain.py subs get
./terrain.py subs get --user username
./terrain.py subs get -u username

options:
  --user username, -u username
                        the username of the user to get subscription informaton for

Gets information about the current subscription. If the username is not provided
or happens to be the username of the currently authenticated user then admin
access is not required and the user's current subscription is displayed.

If the username is provided and is not the username of the currently authenticated
user then admin access is required. If the authenticated user has admin access then
information about the currently active subscription of the specified user will be
displayed.

./terrain.py subs add --user username --plan plan
./terrain.py subs add -u username -p plan

options:
  --user usermame, -u username
                        the username of the user to create the subscription for
  --plan plan_name, -p plan_name
                        the name of the plan to subscribe the user to

Subscribes a user to a plan. The plan will be effective as of the time the command
is processed, and it will expire after one year. Admin accessis is required to use
this command.

./terrain.py subs help

Display this help message.
```

# Terrain CLI

Command-Line interface for the CyVerse Terrain API.

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

If th e username argument is specified and not equal to the username of the authenticated user then the administrative
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

# Terrain CLI

Command-Line interface for the CyVerse Terrain API.

## Using Docker

This utility is available in CyVerse's image repository: `harbor.cyverse.org/de/terrain-cli:0.0.1`. When you launch this
container, it will display a shell prompt where you can run commands interactively:

```
root@d8440e584e6b:/# terrain help

The following subcommands are available:

    help: list available subcommands
    subscriptions: subscription operations (subscription,sub,subs)
```

## Usage

### Getting Help

Aliases: `help`

Lists available subcommands:

```
$ ./terrain.py help

The following subcommands are available:

    help: list available subcommands
    subscriptions: subscription operations (subscription,sub,subs)
```

### Subscriptions

Aliases: `subscriptions`, `subscription`, `sub`, `subs`

The subscriptions subcommand provides a command-line interface to API endpoints that can query and update subscription
information. Please see the [subscriptions subcommand documentation][1] for additional
documentation.

[1]: docs/subscriptions.md

# Subscriptions

Aliases: `subscriptions`, `subscription`, `sub`, `subs`

The subscriptions subcommand is used to check and manage user subscriptions. This subcommand has the following aliases:
`subscriptions`, `subscription`, `subs`, `sub`. All of these aliases are equivalent; feel free to use whichever feels
the most natural.

## Listing Plans

Aliases: `list-plans`, `plans`, `lp`

In order to create a subscription, it's necessary to know which subscription plans are available. The `list-plans`
subcommand (a.k.a. `plans`, `lp`) will display information about each of the avialble plans:

```
$ terrain subscriptions list-plans
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

The output contains the list of plan names along with the quotas associated with each plan.

## Listing Resource Types

Aliases: `list-resource-types`, `resource-types`, `lrt`, `rt`

The resource types are fairly self-explanatory, but there's no guarantee that each subscription plan will have a quota
for every available resource type. To get a complete list of resource types, you can use the `list-resource-types`
(a.k.a. `resource-types`, `lrt`, `rt`) subcommand:

```
$ terrain subscriptions list-resource-types
cpu.hours: cpu hours
data.size: bytes
```

Each line in the output of this subcommand contains the resource type name followed by a brief description of the unit
used by the resource type.

## Displaying the Current Subscription

Aliases: `get`

If you want to display information about a user's current subscription plan, you can use the `get` subcommand. This
command comes in two flavors. Anyone can get information about their own subscription like this:

```
$ terrain subscriptions get
Effective Starting: 2023-01-04T17:46:29.357179-07:00
Expires At: 2024-01-04T17:46:29.357179-07:00
Plan: Pro
Quotas:
    cpu.hours: 2000.0
    data.size: 3298534883328.0
Usages:
```

Administrators can use the optional `--user` (a.k.a. `-u`) argument to get information about another user's current
subscription plan:

```
$ terrain subscriptions get --user=ipctest
Effective Starting: 2022-11-28T21:04:59.134491-07:00
Expires At: 2023-11-28T21:04:59.134491-07:00
Plan: Commercial
Quotas:
    cpu.hours: 5000.0
    data.size: 5497558138880.0
Usages:
    cpu.hours: 424.61312672999986
    data.size: 181347698.0
```

As an extra measure of safety, an error message will be displayed if you specify a non-existent username:

```
$ terrain subscriptions get --user=idonotexist
user does not exist: idonotexist
```

## Adding Subscriptions

Aliases: `add`

Administrators have the ability to create new subscription plans for users using the `add` subcommand:

```
$ terrain subscriptions add --user=ipcdev --plan=commercial
Effective Starting: 2023-01-04T17:59:29.985629-07:00
Expires At: 2024-01-04T17:59:29.985629-07:00
Plan: Commercial
Quotas:
    cpu.hours: 5000.0
    data.size: 5497558138880.0
Usages:
```

The arguments for this command are also validated. If you enter an incorrect username, you'll get this:

```
$ terrain subscriptions add --user=idonotexist --plan=commercial
user does not exist: idonotexist
```

If you enter an incorrect plan name, you'll get this:

```
$ terrain subscriptions add --user=ipcdev --plan=bogus
plan does not exist: bogus
```

It's also possible for an administrator to give themselves a new subscription, but they have to specify their own
username using the `--user` argument to do so. Failure to specify this argument will result in an error:

```
$ terrain subscriptions add --plan=commercial
usage: Terrain API Client subscriptions add [-h] -u USER -p PLAN
Terrain API Client subscriptions add: error: the following arguments are required: -u/--user
```

## Setting Quotas

Aliases: `set-quota`

Administrators have the ability to set a user's quota to a different value using the `set-quota` subcommand:

```
$ terrain subscriptions set-quota --user=ipcdev --resource-type=cpu.hours --quota=20000
Effective Starting: 2023-01-04T17:59:29.985629-07:00
Expires At: 2024-01-04T17:59:29.985629-07:00
Plan: Commercial
Quotas:
    cpu.hours: 20000.0
    data.size: 5497558138880.0
Usages:
    data.size: 9165.0
```

The quota can be specified as a raw number (as in the example above) or using one of the following modifiers:

| Modifier     | Value      |
| ------------ | ---------- |
| 'K' or 'k'   | 2^10       |
| 'M' or 'm'   | 2^20       |
| 'G' or 'g'   | 2^30       |
| 'T' or 't'   | 2^40       |

When specifying data storage quotas, this allows you to use something like `10t` to mean `10 TiB`, for example:

```
$ terrain subscriptions set-quota --user=ipcdev --resource-type=data.size --quota=10t
Effective Starting: 2023-01-04T17:59:29.985629-07:00
Expires At: 2024-01-04T17:59:29.985629-07:00
Plan: Commercial
Quotas:
    cpu.hours: 20000.0
    data.size: 10995116277760.0
Usages:
    data.size: 9165.0
```

You can also use these modifiers for other resource types, but they're not generally as useful in those cases.

Once again, the arguments are all validated:

```
$ terrain subscriptions set-quota --user=idonotexist --resource-type=data.size --quota=10t
user does not exist: idonotexist

$ terrain subscriptions set-quota --user=ipcdev --resource-type=not.real --quota=10t
resource type does not exist: not.real

$ terrain subscriptions set-quota --user=ipcdev --resource-type=data.size --quota=10x
invalid quota specification: 10x
```

The `--user`, `--resource-type` and `--quota` arguments are also all required, meaning that administrators can update
their own quotas but they must specify their own usernames using the `--user` argument to do so.

## Getting Help

Aliases: `help`

To get a brief usage summary for this subcommand, you can so this:

```
$ terrain subscriptions help
```

#!/usr/bin/env python3

import getpass
import jwt
import os
import os.path
import stat
import requests
import sys

terrain_base_urls = {
    "prod": "https://de.cyverse.org/terrain",
    "qa": "https://qa.cyverse.org/terrain",
}

def terrain_uri(environment, path):
    """
    Builds a URI that can be used to connect to Terrain.
    """
    base = terrain_base_urls[environment] if environment in terrain_base_urls else None
    if not base:
        raise Exception("invalid terrain environment: {0}".format(environment))
    return "{0}{1}".format(base, path)

def get_auth_token(environment, username, password):
    """
    Gets the authentication token for Terrain.
    """
    uri = terrain_uri(environment, "/token/keycloak")
    r = requests.get(uri, auth=(username, password))
    if r.status_code == 401:
        print("invalid credentials; please try again")
        return None
    if r.status_code < 200 or r.status_code > 299:
        print("unable to authenticate to Terrain", file=sys.stderr)
        sys.exit(1)
    return r.json()["access_token"]

def terrain_auth_file(environment):
    """
    Returns the Terrain auth token file path for the given environment.
    """
    return "{0}/.terrain-{1}".format(os.environ["HOME"], environment)

def get_cached_access_token(environment):
    """
    Attempts to obtain the access token from $HOME/.terrain-{environment}.
    """
    token = None
    auth_file = terrain_auth_file(environment)
    if os.path.isfile(auth_file):
        with open(auth_file) as f:
            token = f.readline()
    return token if jwt.valid(token) else None

def get_username():
    """
    Prompts the user for the username to use to authenticate to Terrain.
    """
    print("Username: ", end="", flush=True)
    return sys.stdin.readline().strip()

def get_password():
    """
    Prompts the user for the password to use to authenticate to Terrain.
    """
    return getpass.getpass(prompt="Password: ")

def authenticate(environment):
    """
    Attempts to obtain an auth token from Terrain.
    """
    token = None
    while token is None:
        username = get_username()
        password = get_password()
        token = get_auth_token(environment, username, password)
    return token

def cache_token(environment, token):
    """
    Stores a copy of the access token in $HOME/.terrain-{environment}.
    """
    auth_file = terrain_auth_file(environment)
    with open(auth_file, "w") as f:
        print(token, file=f)
    os.chmod(auth_file, stat.S_IRUSR | stat.S_IWUSR)

def get_access_token(environment):
    """
    Gets the access token to use for Terrain. The access token will be cached in $HOME/.terrain-{environment}. If
    the file exists and contains an active access token then that token will be used. Otherwise, the user will be
    prompted to log in.
    """
    token = get_cached_access_token(environment)
    if token is None:
        token = authenticate(environment)
        cache_token(environment, token)
    return token.strip()

def add_auth_header(environment, headers):
    """
    Adds the authorization header to the given set of headers to be passed to Terrain.
    """
    headers['Authorization'] = 'Bearer {0}'.format(get_access_token(environment))
    return headers

def list_plans(environment):
    """
    Returns the list of available subscription plans.
    """
    uri = terrain_uri(environment, "/qms/plans")
    r = requests.get(uri, headers=add_auth_header(environment, {}))
    r.raise_for_status()
    return r.json()["result"]

def list_resource_types(environment):
    """
    Returns the list of available resource types.
    """
    uri = terrain_uri(environment, "/qms/resource-types")
    r = requests.get(uri, headers=add_auth_header(environment, {}))
    r.raise_for_status()
    return r.json()["result"]

def get_subscription(environment):
    """
    Returns the currently active subscription for the authenticated user.
    """
    uri = terrain_uri(environment, "/qms/user/plan")
    r = requests.get(uri, headers=add_auth_header(environment, {}))
    r.raise_for_status()
    return r.json()["result"]

def admin_get_subscription(environment, username):
    """
    Returns the currently active subscription for the given user.
    """
    uri = terrain_uri(environment, "/admin/qms/users/{0}/plan".format(username))
    r = requests.get(uri, headers=add_auth_header(environment, {}))
    r.raise_for_status()
    return r.json()["result"]

def admin_add_subscription(environment, username, plan):
    """
    Subscribes a user to a plan.
    """
    uri = terrain_uri(environment, "/admin/qms/users/{0}/plan/{1}".format(username, plan))
    r = requests.put(uri, headers=add_auth_header(environment, {}))
    r.raise_for_status()
    return r.json()

def admin_set_quota(environment, username, resource_type, quota):
    """
    Sets the quota associated with a resuource type in the user's current subscription.
    """
    uri = terrain_uri(environment, "/admin/qms/users/{0}/plan/{1}/quota".format(username, resource_type))
    payload = {"quota": quota}
    r = requests.post(uri, headers=add_auth_header(environment, {}), json=payload)
    r.raise_for_status()
    return r.json()["result"]

def is_valid_username(environment, username):
    """
    Determines whether or not the provided username is valid.
    """
    uri = terrain_uri(environment, "/subjects")
    payload = {"search": username}
    r = requests.get(uri, headers=add_auth_header(environment, {}), params=payload)
    r.raise_for_status()
    for subject in r.json()["subjects"]:
        if subject["id"] == username:
            return True
    return False

def validate_plan_name(environment, plan_name):
    """
    Determines whether or not the provided plan name is valid.
    """
    plans = list_plans(environment)
    for plan in plans:
        if plan["name"].lower() == plan_name.lower():
            return plan["name"]
    return None

def validate_resource_type_name(environment, resource_type_name):
    """
    Determines whether or not the provided resource type name is valid.
    """
    resource_types = list_resource_types(environment)
    for resource_type in resource_types:
        if resource_type["name"].lower() == resource_type_name.lower():
            return resource_type["name"]
    return None

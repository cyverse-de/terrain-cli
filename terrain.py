#!/usr/bin/env python3

import argparse
import base64
import getpass
import jwt
import os
import os.path
import requests
import stat
import sys

terrain_base_urls = {
    "prod": "https://de.cyverse.org/terrain",
    "qa": "https://qa.cyverse.org/terrain",
}

def terrain_auth_file(environment):
    """
    Returns the Terrain auth token file path for the given environment.
    """
    return "{0}/.terrain-{1}".format(os.environ["HOME"], environment)

def get_cached_access_token(environment):
    """
    Attempts to obtain the access token from $HOME/.terrain-auth-{environment}.
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
    Stores a copy of the access token in $HOME/.terrain-auth-{environment}.
    """
    auth_file = terrain_auth_file(environment)
    with open(auth_file, "w") as f:
        print(token, file=f)
    os.chmod(auth_file, stat.S_IRUSR | stat.S_IWUSR)

def get_access_token(environment):
    """
    Gets the access token to use for Terrain. The access token will be cached in $HOME/.terrain-auth-{environment}. If
    the file exists and contains an active access token then that token will be used. Otherwise, the user will be
    prompted to log in.
    """
    token = get_cached_access_token(environment)
    if token is None:
        token = authenticate(environment)
        cache_token(environment, token)
    return token

def parse_args():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser("Terrain API Client")
    parser.add_argument(
        "-e", "--env",
        help="the DE environment to work with",
        choices=["prod", "qa"]
    )
    return parser.parse_args()

def main():
    """
    Authenticates the user if necessary then launches the appropriate subcommand.
    """

    # Parse the command-line arguments.
    args = parse_args()

    # Get the access token.
    token = get_access_token(args.env)

if __name__ == "__main__":
    main()

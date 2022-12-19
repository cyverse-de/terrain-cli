#!/usr/bin/env python3

import base64
import datetime
import json
import pprint

def extract_payload(token):
    """
    Extracts the payload from a JWT.
    """
    payload = token.split(".", 3)[1] + '==' if token is not None else ""
    return json.loads(base64.b64decode(payload)) if payload != "" else None

def get_username(token):
    """
    Returns the username of the authenticated user.
    """
    if token is None or token == "":
        return None
    payload = extract_payload(token)
    return payload["preferred_username"] if "preferred_username" in payload else None

def valid(token):
    """
    Determines whether or not a JWT appears to be valid. For the time being, a JWT is considered to be valid if the
    current time is between the JWT's not-before and expiration timestamps.
    """
    if token is None or token == "":
        return False
    payload = extract_payload(token)
    current_time = datetime.datetime.now()
    nbf = datetime.datetime.fromtimestamp(payload["nbf"]) if "nbf" in payload else None
    if nbf is not None and nbf > current_time:
        return False
    exp = datetime.datetime.fromtimestamp(payload["exp"]) if "exp" in payload else None
    if exp is not None and exp < current_time:
        return False
    return True

#!/usr/bin/env python3

# OPNSense Rule Toggler Copyright (C) 2024 Quinn Luetzow
# This file is part of OPNSense Rule Toggler.

# OPNSense Rule Toggler is free software: you can
# redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.

# OPNSense Rule Toggler is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with OPNSense Rule Toggler. If not, see
# <https://www.gnu.org/licenses/>.


"""
Script for enabling/disabling an automation rule via the OPNSense API.

When enabled the rule will be enforced.
When disabled the rule will not be enforced.

Usage (*Nix):
python3 opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host \
    uuid api_key api_secret -e|--enable|-d|--disable

Usage (Windows):
python opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host \
    uuid api_key api_secret -e|--enable|-d|--disable

Arguments:
    -h, --help        Show this help message and exit.
    -v, --version     Show program version and exit.
    opnsense_host     IP address or FQDN or OPNSense.
    uuid              UUID of automation rule to be enabled/disabled.
    api_key           API key for OPNSense.
    api_secret        API secret for OPNSense.
    -e, --enable      Enable automation rule in OPNSense.
    -d, --disable     Disable automation rule in OPNSense.
"""

__author__ = "Quinn Luetzow"
__version__ = 1.0

import sys
import requests


class OPNSenseError(Exception):
    """Class to represent OPNSense API errors"""
    pass


class OPNSenseRuleStatus:
    """Class to represent a status for the OPNSense filter rule"""

    def __init__(self, status):
        self.self = self
        self.status = status


class OPNSenseData:
    """Class to contain data used to create OPNSense API requests."""

    # Content Type header for the API requests.
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # no actual instances of this class should exist
    def __init__(self):
        pass


def get_current_status(host, rule_uuid, credentials):
    """Get current status of the filter rule from the OPNSense API."""

    # make one GET request to the API.
    # pulls current status of filter rule.
    with requests.session() as session:
        try:
            response = session.get(
                f"https://{host}/api/firewall/filter/getRule/{rule_uuid}",
                headers=OPNSenseData.headers,
                verify=True,
                auth=credentials
            )

        # catch errors from requests module - no recovery possible if it fails, as
        # a connection error or refusal would be on the API side, so re-throw it.
        except requests.exceptions.RequestException as e:
            raise e

    data = response.json()

    if data["rule"]["enabled"] == "1":
        return True
    else:
        return False


def toggle_rule(host, rule_uuid, credentials, toggle):
    # make two POST requests to the API.
    # first enables/disables filter rule.
    # second applies changes in OPNSense.
    with requests.session() as session:
        try:
            if toggle is True:
                change = session.post(
                    f"https://{host}/api/firewall/filter/toggleRule/{rule_uuid}/1",
                    headers=OPNSenseData.headers,
                    verify=True,
                    auth=credentials
                )
            else:
                change = session.post(
                    f"https://{host}/api/firewall/filter/toggleRule/{rule_uuid}/0",
                    headers=OPNSenseData.headers,
                    verify=True,
                    auth=credentials
                )

            apply = session.post(
                f"https://{host}/api/firewall/filter/apply",
                headers=OPNSenseData.headers,
                verify=True,
                auth=credentials
            )

            # catch errors from requests module - no recovery possible if it fails, as
            # a connection error or refusal would be on the API side, so re-throw it.
        except requests.exceptions.RequestException as e:
            raise e

        # check for the correct responses from the API
        if change.json()["changed"] is True and apply.json()["status"].strip() == "OK":
            return True
        else:
            raise OPNSenseError("Failed to set rule status or apply filter changes.")


def main():
    for arg in sys.argv:
        match arg:
            case "-h" | "--help":
                print(__doc__)
                exit(0)
            case "-v" | "--version":
                print(f"OPNSense Rule Toggler version {__version__}")
                exit(0)

    # search for command line args, and if not provided request input from user.
    try:
        opnsense_host = sys.argv[1]
    except IndexError:
        print("OPNSense IP or FQDN: ")
        opnsense_host = input()

    try:
        uuid = sys.argv[2]
    except IndexError:
        print("Automation rule UUID: ")
        uuid = input()

    try:
        api_key = sys.argv[3]
    except IndexError:
        print("API key for OPNSense: ")
        api_key = input()

    try:
        api_secret = sys.argv[4]
    except IndexError:
        print("API secret for OPNSense: ")
        api_secret = input()

    try:
        toggle = sys.argv[5]
    except IndexError:
        print("Enable or disable automation rule (enable/disable): ")
        toggle = input()

    # create tuple for credentials to be passed into http request.
    opnsense_credentials = (api_key, api_secret)

    match toggle:
        case "-e" | "--enable":
            toggle = True
        case "-d" | "--disable":
            toggle = False
        case _:
            raise ValueError(f"Invalid input for desired rule status: {toggle}\n")

    current_status = OPNSenseRuleStatus(get_current_status(opnsense_host, uuid, opnsense_credentials))

    # if neither True nor False, either we've received bad data from the API
    # or the JSON response data format has changed.
    if current_status.status is not True and current_status.status is not False:
        raise OPNSenseError(
            "OPNSense reports neither enabled or disabled for the rule. " +
            "Bad data or the API response was not evaluated correctly. " +
            "The response JSON structure may have changed." +
            f"Reported status is: {str(current_status.status)}")

    # comparing with is because both values are booleans.
    # if user has requested to set rule status to the status it is already in,
    # alert them of that and exit.
    if current_status.status is OPNSenseRuleStatus(toggle).status:
        raise ValueError(f"Automation rule is already {str(current_status.status)}.")

    toggle_rule(opnsense_host, uuid, opnsense_credentials, toggle)

    if toggle is True:
        print("Rule is now enabled.")
    else:
        print("Rule is now disabled.")


if __name__ == "__main__":
    main()

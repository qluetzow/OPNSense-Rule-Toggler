# OPNSense-Rule-Toggler
User interaction and interface with the OPNSense API to utilize automation rules.

Script for enabling/disabling an automation rule via the OPNSense API.

Author: Quinn Luetzow

When enabled the rule will be enforced.
When disabled the rule will not be enforced.

Usage (*Nix): python3 opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host uuid api_key api_secret -e|--enable|-d|--disable

Usage (Windows): python opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host uuid api_key api_secret -e|--enable|-d|--disable

Arguments:
    -h, --help        Show this help message and exit.
    -v, --version     Show program version and exit.
    opnsense_host     IP address or FQDN or OPNSense.
    uuid              UUID of automation rule to be enabled/disabled.
    api_key           API key for OPNSense.
    api_secret        API secret for OPNSense.
    -e, --enable      Enable automation rule in OPNSense.
    -d, --disable     Disable automation rule in OPNSense.
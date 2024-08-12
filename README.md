# OPNSense Rule Toggler
User interaction and interface with the OPNSense API to utilize automation rules.

### Requirements:
* Python >= 3.8
* requests
  - [Documentation](https://requests.readthedocs.io/en/latest/)
  - [Source Code](https://github.com/psf/requests)
  - Install: `pip install requests`


### Usage (*Nix):

`python3 opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host uuid api_key api_secret -e|--enable|-d|--disable`

### Usage (Windows):

`python opensense_rule_toggler.py [-h|--help] [-v|--version] opnsense_host uuid api_key api_secret -e|--enable|-d|--disable`


### Arguments:
* -h, --help       Show this help message and exit.
* -v, --version        Show program version and exit.opnsense_host
* uuid             UUID of automation rule to be enabled/disabled.
* api_key          API key for OPNSense.
* api_secret       API secret for OPNSense.
* -e, --enable     Enable automation rule in OPNSense.
* -d, --disable    Disable automation rule in OPNSense.
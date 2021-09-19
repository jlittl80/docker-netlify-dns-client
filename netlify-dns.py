#!/usr/bin/python3

import os
from urllib import request, parse
import json
import sys
import time

def LogData(message):
    with open("/logs/netlifydns.log", "a") as f:
        f.write(message + '\n')
        print(message)


def getNetlifyDNS(API_TOKEN, DOMAIN, URL):
    ## Build the request for the current DNS entries and execute it
    getreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + DOMAIN + '/dns_records',
                             headers={'Content-Type': 'application/json;charset=utf-8',
                                      'Authorization': 'Bearer ' + API_TOKEN})
    current = json.loads(request.urlopen(getreq).read().decode("utf-8"))

    # Itterate over each DNS entry and return the info from the one we want
    for entry in current:
        if entry['hostname'] == URL.replace("_", "."):
            return entry['id'], entry['type'], entry['value']
    # We didnt match any of them, break
    LogData("DNS entry doesnt exist. Couldn't find a [hostname] that matches the URL")
    raise Exception("DNS entry doesnt exist. Couldn't find a [hostname] that matches the URL")


def AddNetlifyDNS(API_TOKEN, DOMAIN, URL, CURRENTIP):
    # Get the old DNS entry
    oldData = getNetlifyDNS(API_TOKEN, DOMAIN, URL)
    # If the current IP hasnt changed VS the old IP in the DNS entry, dont bother
    if CURRENTIP == oldData[2]:
        LogData("IP hasn't changed. Returning")
        return
    else:
        LogData("Changing IP's from " + oldData[2] + " to " + CURRENTIP)

        # Build the network requests to add & delete the enteries
        netlify_add_req = {}
        netlify_add_req['hostname'] = URL.replace("_", ".")
        netlify_add_req['ttl'] = 3600
        netlify_add_req['type'] = oldData[1]
        netlify_add_req['value'] = CURRENTIP
        netlify_del_req = {}

        request_body = json.dumps(netlify_add_req).encode('utf-8')
        request_del_body = json.dumps(netlify_del_req).encode('utf-8')

        # Add the new DNS record
        actualreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + DOMAIN + '/dns_records')
        actualreq.add_header("Content-Type", "application/json; charset=utf-8")
        actualreq.add_header("Authorization", "Bearer " + API_TOKEN)
        actualreq.add_header('Content-Length', len(request_body))
        response = request.urlopen(actualreq, request_body)
        LogData("Added the NEW data")

        # And remove the old one
        delreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + DOMAIN + '/dns_records/' + oldData[0], method='DELETE')
        delreq.add_header("Content-Type", "application/json; charset=utf-8")
        delreq.add_header("Authorization", "Bearer " + API_TOKEN)
        delreq.add_header('Content-Length', len(request_del_body))
        response_del = request.urlopen(delreq, request_del_body)
        LogData("Deleted the OLD data")

        # Log that the operation succeeded
        newData = getNetlifyDNS(API_TOKEN, DOMAIN, URL)
        LogData("Changed IP's from " + oldData[2] + " to " + newData[2])


def run():
    # Get the API_TOKEN
    try:
        API_TOKEN = os.environ['NETLIFY_API_TOKEN']
        LogData("Got the API token")
    except:
        LogData("Couldn't Get API_TOKEN evn var")
        sys.exit(1)

    # Get the URL to modify, and split it to get the DOMAIN
    try:
        URL = os.environ['NETLIFY_URL']
        splitURL = URL.split("_")
        if len(splitURL) < 2:
            raise Exception("URL isnt long enough")
        DOMAIN = splitURL[(len(splitURL) - 2)] + "_" + splitURL[(len(splitURL) - 1)]
        LogData("Got the URL and DOMAIN. URL: " + URL + ", DOMAIN: " + DOMAIN)
    except:
        LogData("There was a issue with the URL provided")
        sys.exit(1)

    try:
        # Get the CURRENT IP from the interwebs, and start the AddNetlifyDNS function
        ipresp = json.loads(request.urlopen('https://api.ipify.org?format=json').read().decode("utf-8"))
        CURRENTIP = ipresp['ip']

        LogData("Got the Current IP, starting. IP: " + CURRENTIP)
        AddNetlifyDNS(API_TOKEN, DOMAIN, URL, CURRENTIP)
    except:
        # Unlucky if we are here
        LogData("Something broke")


if __name__ == '__main__':
    # These need to be exported for this to work
    # export NETLIFY_API_TOKEN=XXXXXXXXXXXXX
    # export NETLIFY_URL

    while True:
        LogData("Starting")
        run()
        LogData("Sleeping")
        time.sleep(1800)

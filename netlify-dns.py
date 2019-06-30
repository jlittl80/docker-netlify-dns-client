#!/usr/bin/python3

import os
from urllib import request, parse
import json
import sys

LOG_FILE = open('/var/log/netlifydns.log', 'w')
oldid = None
oldip = None


def getNetlifyDNS():
    global oldid, oldip
    getreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + urlv1 + '/dns_records',
                             headers={'Content-Type': 'application/json;charset=utf-8',
                                      'Authorization': 'Bearer ' + API_TOKEN})
    current = json.loads(request.urlopen(getreq).read().decode("utf-8"))
    oldid = current[0]['id']
    oldip = current[0]['value']


def AddNetlifyDNS():
    global oldid, oldip
    getNetlifyDNS()
    if ipresp['ip'] == oldip:
        LOG_FILE.write("IP hasn't changed...")
        sys.exit(0)
    else:
        LOG_FILE.write("Changing IP's from " + oldip + " to " + ipresp['ip'])


        netlify_add_req = {}
        netlify_add_req['hostname'] = URL
        netlify_add_req['ttl'] = 3600
        netlify_add_req['type'] = "A"
        netlify_add_req['value'] = ipresp['ip']

        netlify_del_req = {}

        print(netlify_del_req)
        request_body = json.dumps(netlify_add_req).encode('utf-8')
        request_del_body = json.dumps(netlify_del_req).encode('utf-8')

        print("url::" + urlv1)
        actualreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + urlv1 + '/dns_records')
        actualreq.add_header("Content-Type", "application/json; charset=utf-8")
        actualreq.add_header("Authorization", "Bearer " + API_TOKEN)
        actualreq.add_header('Content-Length', len(request_body))
        response = request.urlopen(actualreq, request_body)

        delreq = request.Request('https://api.netlify.com/api/v1/dns_zones/' + urlv1 + '/dns_records/' + oldid, method='DELETE')
        delreq.add_header("Content-Type", "application/json; charset=utf-8")
        delreq.add_header("Authorization", "Bearer " + API_TOKEN)
        delreq.add_header('Content-Length', len(request_del_body))
        response_del = request.urlopen(delreq, request_del_body)

        print(response.read())
        print(response_del.read())



if __name__ == '__main__':
    
    # export NETLIFY_API_TOKEN=XXXXXXXXXXXXX
    try:
        API_TOKEN = os.environ['NETLIFY_API_TOKEN']
    except:
        print("Couldn't Get API_TOKEN evn var")
        sys.exit(1)

    # export NETLIFY_URL
    try:
        URL = os.environ['NETLIFY_URL']
        urlv1 = URL.replace(".com", "_com")
    except:
        print("Couldn't Get API_TOKEN evn var")
        sys.exit(1)

    ipresp = json.loads(request.urlopen('https://api.ipify.org?format=json').read().decode("utf-8"))
    AddNetlifyDNS()

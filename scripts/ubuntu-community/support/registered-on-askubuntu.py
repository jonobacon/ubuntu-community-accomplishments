#!/usr/bin/python
import traceback, sys
import json
import gzip
import simplejson
import urllib2
import StringIO
from accomplishments.daemon import dbusapi

try:
    api = dbusapi.Accomplishments()
    userurl = api.get_extra_information("ubuntu-community", "askubuntu-user-url")
    if bool(userurl[0]["askubuntu-user-url"]) == False:
        sys.exit(1)
    else:
        userurl = userurl[0]["askubuntu-user-url"]

    userid = int(userurl.split("/")[-2])

    try:
        badges_req = urllib2.urlopen('http://api.stackexchange.com/2.0/users/%d/badges?pagesize=100&order=asc&sort=name&site=askubuntu&key=zUuJiog6hjENJovHBpM11Q((' % userid)
    except:
        sys.exit(1)
    
    badges_raw = badges_req.read()

    badges_raw = StringIO.StringIO(badges_raw)
    gzipr = gzip.GzipFile(fileobj=badges_raw)

    badges_raw = gzipr.read()
    badges_data = json.loads(badges_raw)
    
    if len(badges_data['items']) != 0:
        sys.exit(0)

    sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)



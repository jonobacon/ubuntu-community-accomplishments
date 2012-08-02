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

    # API: http://api.stackexchange.com/docs/types/user
    try:
        user_req = urllib2.urlopen('https://api.stackexchange.com/2.0/users/%d?site=askubuntu&key=zUuJiog6hjENJovHBpM11Q((' % userid)

    except:
        sys.exit(1)

    user_raw = user_req.read()
    user_raw = StringIO.StringIO(user_raw)
    gzipr = gzip.GzipFile(fileobj=user_raw)

    user_raw = gzipr.read()
    user_data = json.loads(user_raw)
    user_type = user_data['items'][0]['user_type']

    if user_type == 'registered' or user_type == 'moderator':
        sys.exit(0)
    elif user_type == 'unregistered' or user_type == 'does_not_exist':
        sys.exit(1)
    else:
        print "A new user_type is in the StackExchange API, please report this as a bug and report the new user-type of %s for user %d" % (user_type, userid)
        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)



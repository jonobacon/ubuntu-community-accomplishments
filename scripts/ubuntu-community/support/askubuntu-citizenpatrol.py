#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi
# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from aubadges import AUBadges

try:
    api = dbusapi.Accomplishments()
    userurl = api.get_extra_information("ubuntu-community", "askubuntu-user-url")
    if bool(userurl[0]["askubuntu-user-url"]) == False:
        sys.exit(4)
    else:
        userurl = userurl[0]["askubuntu-user-url"]

    userid = int(userurl.split("/")[-2])
    badgeid = 8

    me = AUBadges.fetch(userid)
    if badgeid in me.badges:
        sys.exit(0)
    else:
        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

#!/usr/bin/python
import traceback, sys
import urllib2
import re

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

try:
    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)

    if me == None:
        sys.exit(1)
    else:
        username = str(me).split("~")[1]
        # we check the current planet config held in bzr for a LP username match
        url = "http://bazaar.launchpad.net/~planet-ubuntu/config/main/view/head:/config.ini"
        html_content = urllib2.urlopen(url).read()
        matches = re.findall(username, html_content)

        if len(matches) == 0:
            sys.exit(1)
        else:
            sys.exit(0)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

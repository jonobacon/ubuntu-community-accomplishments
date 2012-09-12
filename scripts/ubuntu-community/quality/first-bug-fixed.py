#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

try:
    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    # Get count of bugs reported by user from Launchpad, using email to
    # identify
    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        ubuntu=l.projects['ubuntu']
        bugs_reported = ubuntu.searchTasks(assignee=me, 
            status=['Fix Released'])
        if len(bugs_reported) > 0:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

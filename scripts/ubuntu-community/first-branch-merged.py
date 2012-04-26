#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi


try:
    import sys, os, pwd, subprocess
    from launchpadlib.launchpad import Launchpad

    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    # Check if user has at least one merge proposal with
    # 'Merged' status
    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        branches = me.getMergeProposals(status='Merged')
        if len (branches) > 0:
          sys.exit(0)
        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

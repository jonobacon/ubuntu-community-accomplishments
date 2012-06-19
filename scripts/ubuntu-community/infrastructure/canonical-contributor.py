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

    # Check if user is member of contributor-agreement-canonical team, 
    # using email to identify
    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        for team in me.super_teams: 
            if team.name == 'contributor-agreement-canonical':
                sys.exit(0)

        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

#!/usr/bin/python

import traceback, sys
import libaccomplishments

try:
    import json, sys, os, pwd, subprocess
    from ubuntuone.couch import auth
    from launchpadlib.launchpad import Launchpad

    libaccom = libaccomplishments.Accomplishments()

    f = libaccom.getExtraInformation("ubuntu-community", "Launchpad Email")

    if bool(f[0]["Launchpad Email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["Launchpad Email"]

    # Get count of bugs reported by user from Launchpad, using email to identify
    l=Launchpad.login_anonymously('ubuntu-community accomplishments','production')
    me=l.people.getByEmail(email=email)

    if me == None:
        sys.exit(1)
    else:
        ubuntu=l.projects['ubuntu']
        bugs_reported = ubuntu.searchTasks(bug_reporter=me, 
            status=['New', 'Incomplete', 'Invalid', 'Confirmed', 'Triaged', 
            'In Progress', 'Fix Committed', 'Fix Released', 'Opinion', "Won't Fix"])

        print len(bugs_reported)

        if len(bugs_reported) > 0:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)


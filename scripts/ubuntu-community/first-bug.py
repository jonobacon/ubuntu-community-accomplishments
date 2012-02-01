#!/usr/bin/python

import traceback, sys

sys.path.append("/home/jono/source/trophyinfo/daemon")
import libaccomplishments

try:
    import json, sys, os, pwd, subprocess
    from ubuntuone.couch import auth
    from launchpadlib.launchpad import Launchpad

    # Get user's email from Ubuntu One, since we have U1 credentials
    #email = json.loads(auth.request(url='https://one.ubuntu.com/api/account/')[1])['email']
    #email = "jono@ubuntu.com"

    libaccom = libaccomplishments.Accomplishments()
    f = libaccom.getExtraInformation("ubuntu-community", "launchpad-email")
    print 
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    # Get count of bugs reported by user from Launchpad, using email to identify
    l=Launchpad.login_anonymously('ubuntu-community accomplishments','production')
    me=l.people.getByEmail(email=email)
    ubuntu=l.projects['ubuntu']
    bugs_reported = ubuntu.searchTasks(bug_reporter=me, 
        status=['New', 'Incomplete', 'Invalid', 'Confirmed', 'Triaged', 
        'In Progress', 'Fix Committed', 'Fix Released', 'Opinion', "Won't Fix"])
    if len(bugs_reported) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)


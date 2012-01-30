#!/usr/bin/python

import traceback
try:
    import json, sys, os, pwd, subprocess
    from ubuntuone.couch import auth
    from launchpadlib.launchpad import Launchpad

    # Get user's email from Ubuntu One, since we have U1 credentials
    email = "jono@ubuntu.com"

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


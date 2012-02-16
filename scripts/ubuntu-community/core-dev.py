#!/usr/bin/python

import traceback, sys
import libaccomplishments

try:
    import json, sys, os, pwd, subprocess
    from ubuntuone.couch import auth
    from launchpadlib.launchpad import Launchpad

    libaccom = libaccomplishments.Accomplishments()

    f = libaccom.getExtraInformation("ubuntu-community", "launchpad-email")

    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    lp=Launchpad.login_anonymously('ubuntu-community accomplishments','production')
    me=lp.people.getByEmail(email=email)

    user = me.name
    print user

    teams = [team.name for team in lp.people['ubuntu-core-dev'].sub_teams]

    if teams == []:
        teams.append(lp.people['ubuntu-core-dev'].name)

    try:
        memberships = [
            membership for membership in
            lp.people[user].memberships_details
            if membership.team_link.rsplit('~', 1)[-1] in
                ['ubuntu-core-dev'] + teams]
    except KeyError:
        memberships = []

    if memberships:
        print 'Member: %s' % memberships
        sys.exit(0)
    else:
        print "Not a member"
        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)


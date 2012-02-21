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

    if me == None:
        sys.exit(1)
    else:
        user = me.name

        teams = [team.name for team in lp.people['ubuntu-fridge'].sub_teams]

        if teams == []:
            teams.append(lp.people['ubuntu-fridge'].name)

        try:
            memberships = [
                membership for membership in
                lp.people[user].memberships_details
                if membership.team_link.rsplit('~', 1)[-1] in
                    ['ubuntu-fridge'] + teams]
        except KeyError:
            memberships = []

        if memberships:
            print "member of the team"
            sys.exit(0)
        else:
            print "not a member of the team"
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)


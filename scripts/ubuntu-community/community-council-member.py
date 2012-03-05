#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi


try:
    import json, sys, os, pwd, subprocess
    from ubuntuone.couch import auth
    from launchpadlib.launchpad import Launchpad

    api = dbusapi.Accomplishments()
    f = api.getExtraInformation("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)

    if me == None:
        sys.exit(1)
    else:
        user = me.name
        teams = [team.name for team in lp.people['communitycouncil'].sub_teams]
        if teams == []:
            teams.append(lp.people['communitycouncil'].name)
        try:
            memberships = [
                membership for membership in
                lp.people[user].memberships_details
                if membership.team_link.rsplit('~', 1)[-1] in
                    ['communitycouncil'] + teams]
        except KeyError:
            memberships = []
        if memberships:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

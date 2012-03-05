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
        sys.exit(2)
    else:
        email = f[0]["launchpad-email"]
    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        user = me.name
        final = []
        for team in me.super_teams:
            for sup in team.super_teams:
                if "locoteams" in sup.self_link.rsplit('~', 1)[-1]:
                    final.append(sup)
        if len(final) is not 0:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi


try:
    import sys, os, pwd, subprocess
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
        if me.is_ubuntu_coc_signer == True:
            sys.exit(0)
        else:
            sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

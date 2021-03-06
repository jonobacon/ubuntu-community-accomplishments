#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi
# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from helpers import Launchpad

try:
    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]
        
    me = Launchpad.fetch(email)
    if "bugsquad" in me.super_teams:
        sys.exit(0)
    else:
        sys.exit(1)

except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

#!/usr/bin/python
import traceback, sys

import datetime

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from loco_team_portal import LocoTeamPortal

GLOBAL_JAM_NAME = 'Ubuntu Global Jam'

try:

    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(2)
    else:
        email = f[0]["launchpad-email"]

    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)
    if me is None:
        sys.exit(1)

    ltp = LocoTeamPortal()
    attending = ltp.getCollection('attendees', attendee_profile__user__username=me.name, promise="sure", team_event__date_begin__lt=datetime.datetime.now(), team_event__global_event__name=GLOBAL_JAM_NAME)
    if len(attending) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
    
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)

#!/usr/bin/python
import traceback, sys

import datetime

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

# Add scripts/lib/ to the PYTHONPATH
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from helpers import LocoTeamPortal

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
    # Get group membership
    member_groups = ltp.getCollection('groups', user__username=me.name)
    member_teams = [member_groups[group_id]['name'] for group_id in member_groups]

    # Get all attended events
    attended_teams = ltp.getCollection('teams', teamevent__attendee__attendee_profile__user__username=me.name, teamevent__attendee__promise="sure", teamevent__date_begin__lt=datetime.datetime.now())

    for team in attended_teams.values():
        # If the user attended an event for a team that they are not a member of, return true
        if team['lp_name'] not in member_teams:
            sys.exit(0)

    sys.exit(1)
    
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
